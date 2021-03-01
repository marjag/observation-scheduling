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
		self.executed = 0
		self.energy = energy_storage
		self.can_observe = int(memory_storage / memory_use)
		self.sat_name = sat_name if sat_name else orbit

	def get(self):
		o = {}
		o['orbit'] = self.orbit
		o['memory_use'] = self.memory_use
		o['energy_use'] = self.energy_use
		o['energy_gen'] = self.energy_gen
		o['memory_storage'] = self.memory_storage
		o['energy_storage'] = self.energy_storage
		o['observe_time'] = self.observe_time
		o['downlink_time'] = self.downlink_time
		o['uplink_time'] = self.uplink_time
		o['busy'] = self.busy
		o['observed'] = self.observed
		o['executed'] = self.executed
		o['can_observe'] = self.can_observe
		o['sat_name'] = self.sat_name
		o['energy'] = self.energy
		return o

