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
	def __init__(self):
		self.done = []
		self.tasks = 0
		self.solutions = []
		s_1 = Satellite("1",10,5,10,10,1,20,10,10,'A')
		s_2 = Satellite("2",20,10,10,20,1,15,10,10,'B')
		# s_3 = Satellite("3",20,10,10,20,1,15,10,10,'C')
		visible_at_all = [s_1.orbit,s_2.orbit]

		t_1 = Task("1",1,50,"O",visible_at_all)
		t_2 = Task("2",25,55,"O",visible_at_all)
		t_3 = Task("3",30,55,"U",visible_at_all)
		t_4 = Task("4",60,80,"O",visible_at_all)
		t_5 = Task("5",80,100,"U",visible_at_all)
		self.run([t_1,t_2],[s_1,s_2])

	def cost(self,task,satellite):
		task_type = 0
		# print ("3 * "+str(satellite.get_observe_time())+"+ 2 * " + str(satellite.memory_use) + " + " + str(satellite.energy_use) + " - " + str(task.get_priority()))
		return 3 * satellite.observe_time + 2 * satellite.memory_use + satellite.energy_use - task.priority

	def can_execute(self,task,satellite):
		return task.is_visible_at(satellite.orbit) and satellite.has_more_memory() and satellite.has_more_energy()


	def add_solution(self,solution):
		solution_ = []
		for task in solution:
			solution_.append(task.serialize())
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
		exit()
		for solution in self.solutions:
			self.print_solution(solution)

	''' Branches '''
	def branch(self,done,rest,satellites):
		for x in range(0,len(satellites)):
			satellites[x] = deepcopy(satellites[x])
		for x in range(0,len(done)):
			done[x] = deepcopy(done[x])
		for x in range(0,len(rest)):
			rest[x] = deepcopy(rest[x])
		if len(rest) < 1:
			if len(done) == self.tasks:
				self.add_solution(done)
			return self.done
		else:
			# analyze current
			rest_ = rest.copy()
			task = rest_.pop(0)
			assignments = self.sat_combinations(task,satellites)
			for sat in assignments:
				# dead branch, do not branch deeper
				if self.is_dead(task,sat):
					pass
				else:
					done_ = done.copy()
					task.assign(sat)
					done_.append(task)
					self.print_node(done_,rest_)
					self.branch(done_,rest_,satellites)

	''' Bounds a branch '''
	def is_dead(self,task,assignment):
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

	'''DEBUG'''

	def print_node(self,done,rest):
		print("done:")
		for task in done:
			assigned = task.get_assigned_to()
			if len(assigned) > 0:
				assigned = ''
				for sat in assigned:
					assigned += sat.sat_name
				# assigned = assigned[0].sat_name
			else:
				assigned = 'not-assigned'

			print("task " + task.task_id + " by " + assigned)

		print("rest:")
		for task in rest:
			print("task " + task.task_id)

		print()

	def print_solution(self,serialized):
		for task in serialized:
			tid = task.get('task_id')
			orbits = []
			for sat in task.get('orbits'):
				orbits.append(str(sat.sat_name))
			
			at = ', '.join(orbits)
			print('task: ' + tid + ', at: ' + at)
			for sat in task.get('orbits'):
				print(sat.sat_name + " busy ")
				print(sat.busy)

		print()

BnB()