#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from itertools import combinations
from task import Task
from satellite import Satellite
from exception import DeadBranchException
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
	def branch(self,done_,rest_,satellites):
		if len(rest_) < 1:
			if len(done_) == self.tasks:
				self.add_solution(done_)
			return self.done
		else:
			# analyze current
			rest = deepcopy(rest_)
			task_ = rest.pop(0)
			# print(satellites_)
			assignments = self.sat_combinations(task_,satellites)
			for assign in assignments:
				done = deepcopy(done_)
				task = deepcopy(task_)
				try:
					self.is_dead(task,assign)
					copy = []
					print("task " + task.get('task_id') + " by "+str(len(assign))+': ' + self.sats_name(assign))
					for Sat in satellites:
						if Sat in assign:
							Sat = deepcopy(Sat)
							start = task.get('w_start')
							end = start+self.get_action_time(Sat,task)
							self.set_busy(Sat,start,end)
							self.assign(task,Sat,start,end)
							self.propagate_action(task,Sat)
						copy.append(Sat)
					done.append(task)
					self.branch(done,rest,copy)
				except DeadBranchException as e:
					# dead branch, last node, return what was done
					self.branch(done,[],[])


	''' Bounds a branch '''
	def is_dead(self,task,assignment):
		# execute action at max|min orbits bounds (cardinality)
		assigned_cnt = len(assignment)
		if assigned_cnt > task.get('cardinality_max') or assigned_cnt < task.get('cardinality_min'):
			raise DeadBranchException("Dead, to much assigned to a task")

		# visibility bounds, non-concurrent actions bounds
		for sat in assignment:
			name = sat.get('sat_name')
			# memory|energy bounds
			if not self.has_memory_to(task,sat):
				raise DeadBranchException("Dead, no memory at "+name)
			# if self.execute_window_start(sat,task) == 0:

		# uplink at all visible orbits
		if task.get('task_type') == 'U':
			if len(task.get('visible_at')) != len(assignment):
				id_ = task.get('task_id')
				raise DeadBranchException("Uplink "+ id_ + " should use all visible orbits")
		return False

	def sat_combinations(self,task,satellites):
		# return [[satellites[0]],[satellites[1]]]
		result = []
		for x in range(1,len(satellites)+1):
			c = list(combinations(satellites, x))
			for x in c:
				result.append(x)
		return result

	def assign(self,task,Sat,start,end):
		orbit = Sat.get('orbit')
		task['assigned_to'].append([orbit,start,end-1])
		return task

	def propagate_action(self,task,sat):
		t_type = task.get('task_type')
		if t_type == 'O':
			self.increment_observed(sat)
		elif t_type == 'D':
			sat['observed'] = 0
		elif t_type == 'U':
			pass
		sat['energy'] = sat.get('energy') - sat.get('energy_use')

	def has_more_memory(self,sat):
		return sat.get('observed') < sat.get('can_observe')

	def has_more_energy(self,sat,time):
		return True

	def increment_observed(self,sat):
		sat['observed'] = sat.get('observed') + 1

	def is_visible_at(self,task,sat):
		return sat.get('sat_name') in task.get('visible_at')

	def is_assigned(self,task):
		return len(task.get('assigned_to')) > 0

	def get_assigned_to(self,task):
		return task.get('assigned_to');

	def get_action_time(self,Sat,task):
		if task.get('task_type') == 'O':
			return Sat.get('observe_time')
		elif task.get('task_type') == 'D':
			return Sat.get('downlink_time')
		elif task.get('task_type') == 'U':
			return Sat.get('uplink_time')
		raise DeadBranchException("Bad task type")

	def set_busy(self,Sat,from_,to):
		for x in range(from_,to):
			Sat['busy'].append(x)

	def is_busy_at(self,Sat,time):
		return (time in Sat.get('busy'))

	def has_memory_to(self,task,satellite):
		if task.get('task_type') == 'O':
			if not self.has_more_memory(satellite):
				return False
		return True

	def can_start_at(task,satellite,time):
		return self.is_visible_at(task,satellite) and self.has_more_energy(satellite,time)

	def execute_window_start(self,sat,task):
		execute_duration = sat.get('observe_time')
		t_window_duration = task.get('w_end') - task.get('w_start')
		time = task.get('w_start') - 1
		while time < task.get('w_end') - execute_duration:
			time += 1
			if self.is_busy_at(sat,time) or !self.can_start_at(task,sat,time):
				continue
			return time
		raise DeadBranchException("Dead, no available window at "+name)


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
			assigned_to = task.get('assigned_to')
			print(tid)
			for assignment in assigned_to:
				print(assignment)
			
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
