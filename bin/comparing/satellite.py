#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

	def get_energy_use(self):
		return self.energy_use

	def get_memory_use(self):
		return self.memory_use

	def get_energy_gen(self):
		return self.energy_gen

	def get_observe_time(self):
		return self.observe_time

	def get_downlink_time(self):
		return self.downlink_time

	def get_uplink_time(self):
		return self.uplink_time

	def get_memory_storage(self):
		return self.memory_storage

	def get_energy_storage(self):
		return self.energy_storage

	def get_orbit(self):
		return self.orbit

	def has_more_memory(self):
		return self.observed < self.can_observe

	def has_more_energy(self):
		return True

	def increment_observed(self):
		self.observed += 1

	def set_busy(self,from_,to):
		for x in range(from_,to):
			self.busy.append(x)

	def is_busy_at(self,time):
		return (time in self.busy)

