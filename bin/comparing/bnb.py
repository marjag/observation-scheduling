#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time
from copy import deepcopy
from itertools import combinations
from task import Task
from satellite import Satellite
from exception import DeadBranchException
from exception import InvalidSolutionException
from operator import itemgetter
'''
Class BnB
'''
class BnB:
	def __init__(self):
		self.tasks = 0
		self.timer = 0
		self.done = []
		self.solutions = []
		self.solution_best = {'tasks': [], 'quality': 0}

	def cost(self,task,satellite):
		task_type = 0
		return 3 * satellite.get('observe_time') + 2 * satellite.get('memory_use') + satellite.get('energy_use') - task.get('priority')

	def quality(self,solution):
		quality = 0;
		for done in solution:
			quality += done.get('priority')

	''' Adds correct solution '''
	def add_solution(self,scheduled_tasks):
		solution = {'tasks': [], 'quality': 0}
		for task in scheduled_tasks:
			solution['tasks'].append(task)
			solution['quality'] += task.get('priority') if task.get('assigned_to') else 0
		if solution.get('quality') > self.solution_best.get('quality'):
			self.solution_best = solution
		self.solutions.append(solution)

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
	def run(self,tasks,satellites,max_solutions=50):
		self.timer = 0
		self.done = []
		self.solutions = []
		self.tasks = len(tasks)
		timer = time()
		self.branch([],tasks,satellites)
		self.solutions = sorted(self.solutions, key=itemgetter('quality'))
		self.timer = time() - timer
		if max_solutions > 0:
			start_index = len(self.solutions) - max_solutions
			return self.solutions[start_index:]
		return self.solutions
		
	''' Branches '''
	def branch(self,done_,rest_,satellites):
		if len(rest_) < 1:
			self.add_solution(done_)
			return self.done
		else:
			# analyze Task
			rest = deepcopy(rest_)
			task_ = rest.pop(0)
			assignments = self.sat_combinations(task_,satellites)
			for assign in assignments:
				# print(self.sats_name(assign))
				done = deepcopy(done_)
				task = deepcopy(task_)
				try:
					self.bound(task,assign)
					copy = []
					for Sat in satellites:
						if Sat in assign:
							Sat = deepcopy(Sat)
							start = self.execute_window_start(Sat,task)
							end = start+self.get_action_time(Sat,task)
							self.set_busy(Sat,start,end)
							self.assign(task,Sat,start,end)
							self.propagate_action(task,Sat,start,end)
						copy.append(Sat)
					done.append(task)
					self.branch(done,rest,copy)
				except DeadBranchException as e:
					# dead branch, last node, return what was done
					if self.is_valid_solution(task,rest):
						self.add_solution(done)
						# self.branch(done_,[],[])
				except InvalidSolutionException as e:
					pass


	''' Bounds a branch '''
	def bound(self,task,assignment):
		# execute action at max|min orbits bounds (cardinality)
		assigned_cnt = len(assignment)
		cardinality_max = task.get('cardinality_max')
		if task.get('task_type') == 'O':
			if assigned_cnt > cardinality_max:
				raise DeadBranchException("Dead, must be done in max {max} orbits".format(max=cardinality_max), task, assignment)
		# visibility bounds, non-concurrent actions bounds
		for sat in assignment:
			name = sat.get('sat_name')
			# memory
			if not self.has_memory_to(task,sat):
				raise DeadBranchException("Dead, no memory at "+name, task, assignment)
			if not self.is_visible_at(task,sat):
				raise DeadBranchException("Dead, not visible at "+name, task, assignment)
		# if uplink - at all visible orbits
		if task.get('task_type') == 'U':
			if len(task.get('visible_at')) != len(assignment):
				id_ = str(task.get('task_id'))
				raise InvalidSolutionException("Uplink "+ id_ + " should use all visible orbits")

	''' Returns true when given state is a valid solution '''
	def is_valid_solution(self,curr_task,rest):
		if curr_task.get('emergency') and len(curr_task.get('assigned_to')) < 1:
			return False
		if curr_task.get('task_type') == 'U' and len(curr_task.get('visible_at')) != len(curr_task.get('assigned_to')):
			return False
		for task in rest:
			if task.get('task_type') == 'U' and len(task.get('visible_at')) != len(task.get('assigned_to')):
				return False
		return True

	'''
	Generates satellite assignments combinations
	returns tuples list: [
		()
		('A')
		('B')
		('A','B')
		...
	]
	'''
	def sat_combinations(self,task,satellites):
		result = []
		# generate combinations of 0,1,2... satellites
		for x in range(0,len(satellites)+1):
			c = list(combinations(satellites, x))
			for x in c:
				result.append(x)
		return result

	''' Assigns satellite to given task with execute window '''
	def assign(self,task,Sat,start,end):
		orbit = Sat.get('orbit')
		task['assigned_to'].append([orbit,start,end-1])
		return task

	''' Applies executing of given task on given state '''
	def propagate_action(self,task,sat,start,end):
		t_type = task.get('task_type')
		if t_type == 'O':
			self.increment_observed(sat)
		elif t_type == 'D':
			sat['observed'] = 0
		elif t_type == 'U':
			pass
		sat['energy'] = self.sat_energy_at(sat,start)
		sat['executed'] = sat.get('executed') + 1

	''' Tests whether satellite at orbit on given state has memory amount to perform observe action '''
	def has_more_memory(self,sat):
		return sat.get('observed') < sat.get('can_observe')

	''' Tests whether satellite at orbit on given state has energy amount to perform action '''
	def has_more_energy(self,sat,time):
		energy_state_at = self.sat_energy_at(sat,time)
		return energy_state_at >= sat.get('energy_use')

	''' Energy calculate formula '''
	def sat_energy_at(self,sat,time):
		return sat.get('energy_storage') + time * sat.get('energy_gen') - (sat.get('executed') * sat.get('energy_use'))

	''' Increments orbit's observed counter '''
	def increment_observed(self,sat):
		sat['observed'] = sat.get('observed') + 1

	''' Returns True when given task is visible for a given orbit's satellite '''
	def is_visible_at(self,task,sat):
		return sat.get('orbit') in task.get('visible_at')

	''' Returns True when task has any assignments '''
	def is_assigned(self,task):
		return len(task.get('assigned_to')) > 0

	''' Returns task's assignments '''
	def get_assigned_to(self,task):
		return task.get('assigned_to');

	''' Gets given orbit's satellite's execute time for given task '''
	def get_action_time(self,Sat,task):
		if task.get('task_type') == 'O':
			return Sat.get('observe_time')
		elif task.get('task_type') == 'D':
			return Sat.get('downlink_time')
		elif task.get('task_type') == 'U':
			return Sat.get('uplink_time')
		raise Error("Bad task type")

	''' Sets orbit's satellite busy state '''
	def set_busy(self,sat,from_,to):
		sat['busy'] += range(from_, to)

	''' Returns true when given satellite is busy at given state and time '''
	def is_busy_at(self,Sat,time):
		return (time in Sat.get('busy'))

	''' Returns true when given satellite is busy during given period at given state '''
	def is_busy_during(self,sat,from_,to):
		for x in range(from_,to):
			if x in sat.get('busy'):
				return True
		return False

	''' Wraps memory check function at given state with different input task '''
	def has_memory_to(self,task,satellite):
		if task.get('task_type') == 'O':
			if not self.has_more_memory(satellite):
				return False
		return True

	''' Picks execute window start value for given orbit and task '''
	def execute_window_start(self,sat,task):
		execute_duration = self.get_action_time(sat,task)
		t_window_duration = task.get('w_end') - task.get('w_start')
		time = task.get('w_start') - 1

		while time <= task.get('w_end') - execute_duration:
			time += 1
			if self.is_busy_at(sat,time) or not self.has_more_energy(sat,time):
				continue
			else:
				# do not overlap actions, test whether would overlap during:
				if self.is_busy_during(sat,time,time+execute_duration):
					continue

			return time
		raise DeadBranchException("Dead, no available window for {task} at {orb}".format(task=task.get('task_id'),orb=sat.get('sat_name')), task, [sat])


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
		quality = serialized.get('quality')
		tasks = serialized.get('tasks')
		if len(tasks) < 1:
			print("no tasks executed")
			return
		print("scheduled actions:")
		for task in tasks:
			tid = task.get('task_id')
			assigned_to = task.get('assigned_to')
			print(str(tid) + " at:")
			for assignment in assigned_to:
				print("orbit {o} during {start}-{end}".format(o=assignment[0],start=assignment[1],end=assignment[2]))
			
		print("optimisation: {o}".format(o=quality))
		print()

	def print_solutions(self,solutions):
		if len(solutions) < 1:
			print("UNSATISFIED - no solutions found")
			return
		s_num = 0
		for solution in solutions:
			s_num += 1
			print("answer {n}:".format(n=s_num))
			self.print_solution(solution)

	def sats_name(self,satellites):
		names = []
		for sat in satellites:
			names.append(sat.get('sat_name'))
		return ', '.join(names)
