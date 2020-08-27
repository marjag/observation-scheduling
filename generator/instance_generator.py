#!/usr/bin/python
# -*- coding: utf-8 -*-

from Utils import Utils
from random import randrange

tools = Utils()

orbits = 2
mains = {
	"orbits": orbits,
	"tasks": orbits*4,
	"ground_stations": orbits*2,
	"control_stations": orbits*2,
}

problem_instance = {}

# orbits, tasks
rules = []
for main_object in mains.keys():
	rules.append(main_object+"(1;"+str(mains.get(main_object))+")")
	problem_instance[main_object] = rules
	rules = []

# task ordering helper
for task_i in range(1, mains.get('tasks')+1):
	for task_j in range(1, mains.get('tasks')+1):
		decision_var = 0
		if task_i + 1 == task_j:
			decision_var = 1

		rules.append('task_order('+str(task_i)+","+str(task_j)+","+str(decision_var)+")")

# problem_instance['task_order'] = rules
rules = []

# priority
for x in range(1, mains.get('tasks')+1):
	rules.append('priority('+str(x)+","+str(randrange(1, 100))+")")

problem_instance['priority'] = rules
rules = []

# memory storage 
for x in range(1, mains.get('orbits')+1):
	rules.append('memory_storage('+str(x)+","+str(randrange(100, 200))+")")

problem_instance['memory_storage'] = rules
rules = []


# memory use
for x in range(1, mains.get('orbits')+1):
	rules.append('memory_use('+str(x)+","+str(randrange(10, 50))+")")

problem_instance['memory_use'] = rules
rules = []

# energy storage 
for x in range(1, mains.get('orbits')+1):
	rules.append('energy_storage('+str(x)+","+str(randrange(200, 300))+")")

problem_instance['energy_storage'] = rules
rules = []

# energy use
for x in range(1, mains.get('orbits')+1):
	rules.append('energy_use('+str(x)+","+str(randrange(5, 10))+")")

problem_instance['energy_use'] = rules
rules = []

# energy gen
for x in range(1, mains.get('orbits')+1):
	rules.append('energy_gen('+str(x)+","+str(randrange(1, 2))+")")

problem_instance['energy_gen'] = rules
rules = []

# pick orbit for tasks
for task in range(1, mains.get('tasks')+1):
	# chose orbit
	orbit = randrange(1, mains.get('orbits')+1)
	
	for avail_orbit in range(1,mains.get('orbits')+1):
		decision_var = 0
		if avail_orbit == orbit:
			decision_var = 1
		
		rules.append('task_orbit('+str(task)+","+str(orbit)+","+str(decision_var)+")")

problem_instance['task_orbit'] = rules
rules = []

time = 0
# pick task windows
for task in range(1, mains.get('tasks')+1):
	time_i = time + randrange(10,30)
	time_j = time_i + tools.window_time()
	time = time_j
	rules.append('task_window('+str(task)+","+str(time_i)+","+str(time_j)+")")

problem_instance['task_window'] = rules
rules = []


cnt = { 
	'ground': mains.get('ground_stations'),
	'control': mains.get('control_stations')
}

# pick station events
for y in range(1,1 + mains.get('control_stations') + mains.get('ground_stations')):
	# chose orbit
	orbit = randrange(1, mains.get('orbits')+1)
	# chose station
	station_type = 'control'
	roll = randrange(0,2)
	if roll == 1:
		station_type = 'ground'

	if (cnt.get(station_type) == 0):
		if station_type == 'control':
			station_type = 'ground'
		else:
			station_type = 'control'

	cnt[station_type] = cnt.get(station_type) - 1
	time_i = time + randrange(10,40)
	time_j = time_i + tools.window_time()
	time = time_j
	rules.append(station_type+'_window('+str(orbit)+","+str(cnt.get(station_type)+1)+","+str(time_i)+","+str(time_j)+")")

problem_instance['stations_window'] = rules
rules = []


# result
filename = 'problem_instance_' + str(randrange(1000,99999)) + '.lp'
fh = open(filename, 'w+')

for field in problem_instance:
	fh.write("#\r\n")
	# print("# "+field)
	for rule in problem_instance.get(field):
		# print(rule+'.')
		fh.write(rule+'.\r\n')

	# print("")
	fh.write("\r\n")
fh.close()
print("Wygenerowano plik z instancją problemu '{label}'".format(label=filename))

