#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randrange
import json

class Generator:
	def __init__(self, config, utils):
		self.config = config
		self.utils = utils
		self.generated_instances = 0

	def gen(self):
		serialized_instance = self.random_serialized_instance()
		model = self.to_dictionary_model(serialized_instance)
		self.write_dictionary(model)
		facts = self.deserialize_instance(serialized_instance)
		self.write_facts(facts)
		self.generated_instances += 1

	def random_serialized_instance(self):
		probab = self.config.getParam("generating").get("actions_probability")
		probab_obs = probab.get("observe")
		probab_up = probab.get("uplink")
		probab_down = probab.get("downlink")
		probab_emergency = probab.get("emergency")
		probab_visibility = probab.get("visibility")
		model = {
			"sat_memory": [],
			"memory_storage": [],
			"memory_use": [],
			"sat_energy": [],
			"energy_storage": [],
			"energy_use": [],
			"action": [],
			"priority": [],
			"orbit": [],
			"satellite": [],
			"sat_action_time": [],
			"action_window": [],
			"energy_gen": [],
			"visible": [],
			"emergency_task": []
		}
		# constants
		model["action_type"] = [["observe"], ["uplink"], ["downlink"]]

		# randomized
		# draw n orbits (0 - random 3-4)
		n = 2
		# density of actions
		density = 0.2
		action_cnt = 50
		orbits = self.utils.rand_orbits(n)
		# draw orbits action executing parameters
		for orbit in orbits:
			for action in model.get("action_type"):
				if action[0] == 'observe':
					sat_action_time = self.utils.rand_sat_observe_time()
				else:
					sat_action_time = self.utils.rand_sat_link_time()
				satellite = str(orbit)
				model['sat_action_time'].append([satellite,action[0],str(sat_action_time)])

		# draw actions (tasks) to perform
		actions = self.utils.rand_actions(action_cnt, probab_obs, probab_down, probab_up)
		model["action"] = actions

		# draw satellites' technical resources
		for orbit in orbits:
			orbit = str(orbit)
			satellite = orbit
			energy_gen = self.utils.rand_digit()
			memory_use = self.utils.rand_use()
			energy_use = self.utils.rand_use()
			memory_storage = self.utils.rand_storage()
			energy_storage = self.utils.rand_storage()
			initial_energy = energy_storage
			model['orbit'].append([orbit])
			model['satellite'].append([orbit, "sat_"+orbit])
			model["sat_energy"].append([satellite,"0",str(initial_energy)])
			model["sat_memory"].append([satellite,"0","0"])
			model["memory_storage"].append([satellite,str(memory_storage)])
			model["energy_storage"].append([satellite,str(energy_storage)])
			model["memory_use"].append([satellite,str(memory_use)])
			model["energy_use"].append([satellite,str(energy_use)])
			model["energy_gen"].append([satellite,str(energy_gen)])

		# draw actions' priorities, visibility and and its executable time window
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

			for orbit in orbits:
				model['visible'].append(self.utils.rand_visibility(action_index,orbit,probab_visibility))
		
		return model

	def deserialize_instance(self,instance):
		facts = []
		for fact_name in instance.keys():
			for fact in instance.get(fact_name):
				facts.append(fact_name + '(' + ','.join(fact) + ').')
		# facts.sort()
		return facts

	def write_facts(self,facts):
		problems_dir = self.config.getPath("problem_instances_dir")
		fname = problems_dir + 'instance_' + str(self.generated_instances) + '.lp'
		print("zapisywanie w pliku " + fname)
		with open(fname, "w") as f:
			f.write('% Instancja wygenerowana automatycznie\n')
			for fact in facts:
				f.write(fact + '\n')
	
	def to_dictionary_model(self,facts):
		sats = facts.get('satellite')
		sat_memory = facts.get('sat_memory')
		memory_storage = facts.get('memory_storage')
		memory_use = facts.get('memory_use')
		sat_energy = facts.get('sat_energy')
		energy_storage = facts.get('energy_storage')
		energy_use = facts.get('energy_use')
		action = facts.get('action')
		priority = facts.get('priority')
		sat_action_time = facts.get('sat_action_time')
		action_window = facts.get('action_window')
		energy_gen = facts.get('energy_gen')
		visible = facts.get('visible')
		emergency_task = facts.get('emergency_task')
		action_type = facts.get('action_type')
		orbits = []
		task_types_symbols = {'observe':'O','uplink':'U','downlink':'D'}

		for x in range(0,len(sats)):
			orbit = {}
			orbit['orbit'] = x + 1
			orbit['sat_name'] = sats[x][1]
			orbit['memory_use'] = int(memory_use[x][1])
			orbit['energy_use'] = int(energy_use[x][1])
			orbit['energy_gen'] = int(energy_gen[x][1])
			orbit['memory_storage'] = int(memory_storage[x][1])
			orbit['energy_storage'] = int(energy_storage[x][1])
			orbit['observe_time'] = int(energy_storage[x][1])
			orbit['busy'] = []
			orbit['executed'] = 0
			orbit['observed'] = 0
			orbit['can_observe'] = int(int(memory_storage[x][1]) / int(memory_use[x][1]))
			sliced = []
			actions_time = sat_action_time[3*x:3*(x+1)]
			for sat,action_type,time in actions_time:
				orbit[action_type+'_time'] = int(time)
			orbits.append(orbit)

		actions = []
		for t_id,t_type in action:
			task = {}
			t_id = int(t_id)
			task['task_type'] = task_types_symbols.get(t_type)
			task['task_id'] = t_id
			task['emergency'] = False
			task['cardinality_min'] = 0
			task['cardinality_max'] = 9999
			task['w_start'] = int(action_window[t_id-1][1])
			task['w_end'] = int(action_window[t_id-1][2])
			task['assigned_to'] = []
			task['visible_at'] = []

			# parse priority
			task['priority'] = 1
			if t_type == 'observe':
				task['cardinality_max'] = 1
				for p_id,prio in priority:
					if int(p_id) == t_id:
						task['priority'] = int(prio)
						break
			# parse visibility
			visible_at = []
			decision_vars = len(sats)
			task_visibility = visible[decision_vars*(t_id-1):decision_vars*(t_id)]
			for x in range(0,len(sats)):
				if task_visibility[x][2] == '1':
					task['visible_at'].append(int(task_visibility[x][1]))
			actions.append(task)

		# parse emergency
		for t_id, in emergency_task:
			actions[int(t_id)-1]['emergency'] = True
			actions[int(t_id)-1]['cardinality_min'] = 1

		return {'orbits': orbits, 'tasks': actions}

	def write_dictionary(self,model):
		fname = self.config.getPath("compare_instances_json")
		print("zapisywanie w pliku " + fname)
		with open(fname, "r+") as f:
			contents = json.loads(f.read())
			f.seek(0)
			contents.get('problems').append(model)
			json.dump(contents, f, indent=4)

