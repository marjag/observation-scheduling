#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from itertools import combinations
from task import Task
from satellite import Satellite
'''
Class BnB
'''
class BnB:
	def __init__(self,tasks,satellites):
		self.done = []
		self.tasks = 0
		self.solutions = []
		self.run(tasks,satellites)

	def cost(self,task,satellite):
		task_type = 0
		# print ("3 * "+str(satellite.get('')get_observe_time())+"+ 2 * " + str(satellite.get('')memory_use) + " + " + str(satellite.get('')energy_use) + " - " + str(task.get_priority()))
		return 3 * satellite.get('observe_time') + 2 * satellite.get('memory_use') + satellite.get('energy_use') - task.get('priority')

	def can_execute(self,task,satellite):
		return task.is_visible_at(satellite.get('orbit')) and has_more_memory(satellite) and has_more_energy(satellite)


	def add_solution(self,solution):
		solution_ = []
		for task in solution:
			solution_.append(task)
		self.solutions.append(solution_)

	'''
	Standard reduction - satellites
	'''
	def minCost(self,task,satellites):
		sat = satellites[0]
		cost_min = self.cost(task,satellites[0])
		for x in range(1, len(satellites)):
			if self.cost(task,satellites[x]) < cost_min:
				sat = satellites[x]
		return sat

	'''
	Runs branch and bound procedure
	'''
	def run(self,tasks,satellites):
		self.tasks = len(tasks)
		self.branch([],tasks,satellites)
		print('finished')
		# exit()
		for solution in self.solutions:
			self.print_solution(solution)

	''' Branches '''
	def branch(self,done,rest,satellites):
		# for x in range(0,len(satellites)):
		# 	satellites[x] = deepcopy(satellites[x])
		if len(rest) < 1:
			if len(done) == self.tasks:
				self.add_solution(done)
			return self.done
		else:
			# analyze current
			rest = deepcopy(rest)
			task = rest.pop(0)
			task = deepcopy(task)
			assignments = self.sat_combinations(task,satellites)
			for sats in assignments:
				sats = deepcopy(sats)
				# dead branch, last node
				if self.is_dead(task,sats):
					pass
					# self.branch(deepcopy(done),[],satellites)
				else:
					print("task " + task.get('task_id') + " by "+str(len(sats))+': ' + self.sats_name(sats) +'\n')
					self.assign(task,sats)
					done.append(task)
					# self.print_node(done_,rest_,satellites)
					self.branch(done,rest,satellites)

	''' Bounds a branch '''
	def is_dead(self,task,assignment):
		return False
		# execute action at max|min orbits bounds (cardinality)
		assigned_cnt = len(assignment)
		if assigned_cnt > task.cardinality_max or assigned_cnt < task.cardinality_min:
			return True

		# visibility bounds, non-concurrent actions bounds
		for sat in assignment:
			# memory|energy bounds
			if not self.can_execute(task,sat):
				return True
			if sat.execute_window_start(task) == 0:
				return True

		# uplink at all visible orbits
		if task.task_type == 'U':
			if len(task.visible_at) != len(assignment):
				return True
		return False

	def sat_combinations(self,task,satellites):
		# satellites = ['A', 'B']
		result = []
		for x in range(1,len(satellites)+1):
			c = list(combinations(satellites, x))
			# c = [x for xs in c for x in xs]
			for x in c:
				result.append(x)
		return result


	def has_more_memory(self,sat):
		return sat.get('observed') < sat.get('can_observe')


	def has_more_energy(self,sat):
		return True

	def increment_observed(self,sat):
		sat['observed'] = sat.get('observed') + 1

	def is_visible_at(self,orbit):
		return orbit in self.visible_at

	def assign(self,Task,satellites):
		for Sat in satellites:
			print(Sat.get('busy'))
			starts = self.execute_window_start(Sat,Task)
			if starts == 0:
				raise Exception("Cannot assign " + Task.get('task_id') + " to " + str(Sat.get('sat_name')) + ", no available window")
			ends = starts + self.get_action_time(Sat,Task)
			self.set_busy(Sat,starts,ends)
			Task['assigned_to'].append(Sat.get('orbit'))

	def is_assigned(self,task):
		return len(task.get('assigned_to')) > 0

	def get_assigned_to(self,task):
		return task.get('assigned_to');

	def get_action_time(self,Sat,Task):
		if Task.get('task_type') == 'O':
			return Sat.get('observe_time')
		elif Task.get('task_type') == 'D':
			return Sat.get('downlink_time')
		elif Task.get('task_type') == 'U':
			return Sat.get('uplink_time')
		raise Exception("Bad task type")

	def set_busy(self,Sat,from_,to):
		for x in range(from_,to):
			Sat['busy'].append(x)
		return Sat

	def is_busy_at(self,Sat,time):
		return (time in Sat.get('busy'))

	def execute_window_start(self,Sat,Task):
		execute_duration = Sat.get('observe_time')
		t_window_duration = Task.get('w_end') - Task.get('w_start')
		time = Task.get('w_start') - 1
		while time < Task.get('w_end') - execute_duration:
			time += 1
			if self.is_busy_at(Sat,time):
				continue
			return time
		return 1


	'''DEBUG'''

	def print_node(self,done,rest,satellites):
		for task in done:
			assigned = task.get_assigned_to()
			if len(assigned) > 0:
				sats = ''
				for sat in assigned:
					sats += sat.sat_name
					print(sat.sat_name + " ")
			else:
				sats = 'not-assigned'

			print("done:")
			print("task " + task.task_id + " by " + sats)

		print("rest:")
		for task in rest:
			print("task " + task.task_id)

		for sat in satellites:
			print("Sat " + sat.sat_name)
			print(sat.busy)
		print()

	def print_solution(self,serialized):
		for task in serialized:
			tid = task.get('task_id')
			orbits = task.get('orbits')
			print(tid)
			print(orbits)
			
			# at = ', '.join(orbits)
			# print('task: ' + tid + ', at: ' + at)
			# for sat in task.get('orbits'):
			# 	print(sat.get('sat_name') + " busy ")
			# 	print(sat.get('busy'))

		print()

	def sats_name(self,satellites):
		names = []
		for sat in satellites:
			names.append(sat.get('sat_name'))
		return ', '.join(names)
