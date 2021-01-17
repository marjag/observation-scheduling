#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randrange
from random import shuffle

class Utils:
	def __init__(self):
		return None

	def rand_orbits(self, cnt=0):
		cnt = cnt if cnt > 0 else randrange(1, len(collection))
		orbits = []
		for x in range(1,cnt+1):
			orbits.append(x)
		return orbits

	def rand_use(self):
		return self.rand_tens()

	def rand_storage(self):
		return self.rand_hundreds()

	def rand_priority(self):
		return randrange(1,50)

	def rand_actions(self, cnt=20, observe=0.80, uplink=0.10, downlink=0.10):
		actions = []
		for x in range(1,cnt+1):
			draw = randrange(0,100) / 100
			if draw < 1 - (observe + downlink):
				a_type = "uplink"
			elif draw < 1 - observe:
				a_type = "downlink"
			else:
				a_type = "observe"

			actions.append([str(x), a_type])
		return actions

	def rand_is_emergency(self,probab=0.10):
		draw = randrange(0,100) / 100
		if draw <= probab:
			return True
		return False

	def rand_visibility(self,action,orbit,probab=0.75):
		draw = randrange(0,100) / 100
		if 1-draw <= probab:
			return [str(action),str(orbit),"1"]
		return [str(action),str(orbit),"0"]

	def rand_digit(self):
		return randrange(1,10)

	'''
	Visibility time window is between 9 and 12 seconds
	'''
	def rand_action_window(self):
		return randrange(9,13)

	'''
	Satellites' observations take time between 9 and 12 seconds
	'''
	# observation
	def rand_sat_observe_time(self):
		return randrange(9,13)

	# communication: downlink, uplink take time between 5 and 9 seconds
	def rand_sat_link_time(self):
		return randrange(5,9)

	# action start uses, proportional to 1 hour schedule:
	# for the density of 1 - action's window start is around
	# action index times random action window duration
	def rand_action_start(self,action,density=0.1):
		density = density if float(density) > 0 else 0.1
		# actions are counted from 1 not from 0, so 
		action = action - 1
		start = action * (self.rand_action_window()/density) + self.rand_digit()
		return int(start)

	def rand_tens(self):
		return self.rand_digit() * 10

	def rand_hundreds(self):
		return self.rand_digit() * 100

	def rand_thousands(self):	
		return self.rand_digit() * 1000

	def rand_filename(self):
		return "instance_" + str(randrange(0, 99999)) + ".lp"

