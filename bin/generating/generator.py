#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randrange

class Generator:
	def __init__(self, config, utils):
		self.config = config
		self.utils = utils

	def gen(self):
		serialized_instance = self.random_serialized_instance()
		facts = self.deserialize_instance(serialized_instance)
		self.write_facts(facts)

	def random_serialized_instance(self):
		probab = self.config.getParam("generating").get("actions_probability")
		probab_obs = probab.get("observe")
		probab_up = probab.get("uplink")
		probab_down = probab.get("downlink")
		probab_emergency = probab.get("emergency")
		model = {
			"sat_memory": [],
			"memory_storage": [],
			"memory_use": [],
			"sat_energy": [],
			"energy_storage": [],
			"energy_use": [],
			"action": [],
			"priority": [],
			"satellite": [],
			"sat_action_time": [],
			"action_window": [],
			"energy_gen": [],
			"emergency_task": []
		}
		# constants
		# 1 hour random instance
		interval = 1800
		model["time"] = [["1.." + str(interval)]]
		model["action_type"] = [["observe"], ["uplink"], ["downlink"]]

		# randomized
		# draw n satellites (0 - random number of satellites)
		n = 3
		# density of actions
		density = 0.2
		action_cnt = 30
		satellites = self.utils.rand_satellites(n)
		# draw satellites action executing parameters
		for sat in satellites:
			for action in model.get("action_type"):
				if action[0] == 'observe':
					sat_action_time = self.utils.rand_sat_observe_time()
				else:
					sat_action_time = self.utils.rand_sat_link_time()
				model['sat_action_time'].append([sat,action[0],str(sat_action_time)])

		# draw actions (tasks) to perform
		actions = self.utils.rand_actions(action_cnt, probab_obs, probab_down, probab_up)
		model["action"] = actions

		# draw satellites' technical resources
		for sat in satellites:
			energy_gen = self.utils.rand_digit()
			memory_use = self.utils.rand_use()
			energy_use = self.utils.rand_use()
			memory_storage = self.utils.rand_storage()
			energy_storage = self.utils.rand_storage()
			initial_energy = energy_storage
			model['satellite'].append([sat])
			model["sat_energy"].append([sat,"0",str(initial_energy)])
			model["sat_memory"].append([sat,"0","0"])
			model["memory_storage"].append([sat,str(memory_storage)])
			model["energy_storage"].append([sat,str(energy_storage)])
			model["memory_use"].append([sat,str(memory_use)])
			model["energy_use"].append([sat,str(energy_use)])
			model["energy_gen"].append([sat,str(energy_gen)])

		# draw actions' priorities and and its executable time window
		has_emergency = False
		action_count = len(actions)
		for action in actions:
			action_index = action[0]
			action_type = action[1]
			a_start = self.utils.rand_action_start(int(action_index),density)
			a_end = a_start + self.utils.rand_action_window()
			model['action_window'].append([str(action_index),str(a_start),str(a_end)])

			if action_type == 'observe':
				model['priority'].append([str(action_index), str(self.utils.rand_priority())])
				# point out emergency tasks
				if not has_emergency or self.utils.rand_is_emergency(probab_emergency):
					model['emergency_task'].append([str(action_index)])
					has_emergency = True

		return model

	def deserialize_instance(self,instance):
		facts = []
		for fact_name in instance.keys():
			for fact in instance.get(fact_name):
				facts.append(fact_name + '(' + ','.join(fact) + ').')
		facts.sort()
		return facts

	def write_facts(self,facts):
		problems_dir = self.config.getPath("problem_instances_dir")
		fname = problems_dir + self.utils.rand_filename()
		print("zapisywanie w pliku " + fname)
		with open(fname, "w") as f:
			f.write('% Instancja wygenerowana automatycznie\n')
			for fact in facts:
				f.write(fact + '\n')
