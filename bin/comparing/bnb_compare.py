#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import copy
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
		s_3 = Satellite("3",20,10,10,20,1,15,10,10,'C')
		visible_at_all = [s_1.get_orbit(),s_2.get_orbit()]

		t_1 = Task("1",1,50,"O",visible_at_all)
		t_2 = Task("2",25,50,"O",visible_at_all)
		t_3 = Task("3",30,55,"D",visible_at_all)
		t_4 = Task("4",60,80,"O",visible_at_all)
		t_5 = Task("5",80,100,"U",visible_at_all)
		print(self.sat_combinations(None,[s_1,s_2,s_3]))
		exit()
		self.run([t_1,t_2,t_3],[s_1,s_2])

	def cost(self,task,satellite):
		task_type = 0
		# print ("3 * "+str(satellite.get_observe_time())+"+ 2 * " + str(satellite.get_memory_use()) + " + " + str(satellite.get_energy_use()) + " - " + str(task.get_priority()))
		return 3 * satellite.get_observe_time() + 2 * satellite.get_memory_use() + satellite.get_energy_use() - task.get_priority()

	def can_execute(self,task,satellite):
		return task.is_visible_at(satellite.orbit) and satellite.has_more_memory() and satellite.has_more_energy()

	def execute_window_start(self,task,satellite):
		execute_duration = satellite.observe_time
		t_window_duration = task.w_end - task.w_start
		time = task.w_start - 1
		print("starts " + str(time))
		while time < task.w_end - execute_duration:
			time += 1
			if satellite.is_busy_at(time):
				continue
		pass

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
		exit(self.sat_combinations(None,satellites))
		self.tasks = len(tasks)
		self.branch([],tasks,satellites)
		print('finished')
		for solution in self.solutions:
			self.print_solution(solution)

	''' Branches '''
	def branch(self,done,rest,satellites):
		done_ = []
		rest_ = []
		if len(rest) < 1:
			if len(done) == self.tasks:
				self.add_solution(done)
			return self.done
		else:
			# analyze current
			rest_ = rest.copy()
			task = rest_.pop(0)
			self.sat_combinations(task,satellites)
			for sat in satellites:
				done_ = done.copy()
				task.assign([sat])
				done_.append(task)
				self.branch(done_,rest_,satellites)



	def sat_combinations(self,task,satellites):
		satellites = ['A', 'B']
		result = []
		for x in range(1,len(satellites)+1):
			c = sorted(combinations(satellites, x))
			result.append(c)
		return result

	'''DEBUG'''

	def print_node(self,done,rest):
		print("done:")
		for task in done:
			assigned = task.get_assigned_to()
			if len(assigned) > 0:
				assigned = assigned[0].sat_name
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
		print()

BnB()