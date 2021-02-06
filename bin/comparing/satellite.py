#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import copy
'''
Class Satellite
'''
class Satellite:
	def __init__(self,orbit,
		memory_use,energy_use,
		energy_gen,
		memory_storage,
		energy_storage,
		observe_time,downlink_time,uplink_time,sat_name=None):
		self.orbit = orbit
		self.memory_use = memory_use
		self.energy_use = energy_use
		self.energy_gen = energy_gen
		self.memory_storage = memory_storage
		self.energy_storage = energy_storage
		self.observe_time = observe_time
		self.downlink_time = downlink_time
		self.uplink_time = uplink_time
		self.busy = []
		self.observed = 0
		self.can_observe = int(memory_storage / memory_use)
		self.sat_name = sat_name if sat_name else orbit

	def get_action_time(self,Task):
		if Task.task_type == 'O':
			return self.observe_time
		elif Task.task_type == 'D':
			return self.downlink_time
		elif Task.task_type == 'U':
			return self.uplink_time
		raise Exception("Bad task type")

	def has_more_memory(self):
		return self.observed < self.can_observe

	def has_more_energy(self):
		return True

	def increment_observed(self):
		self.observed += 1

	def set_busy(self,from_,to):
		self_ = copy(self)
		for x in range(from_,to):
			self_.busy.append(x)
		return self_

	def is_busy_at(self,time):
		return (time in self.busy)

	def execute_window_start(self,Task):
		execute_duration = self.observe_time
		t_window_duration = Task.w_end - Task.w_start
		time = Task.w_start - 1
		while time < Task.w_end - execute_duration:
			time += 1
			if self.is_busy_at(time):
				continue
			return time
		return 0

