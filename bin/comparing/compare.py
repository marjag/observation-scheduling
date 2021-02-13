#!/usr/bin/python3
# -*- coding: utf-8 -*-

from task import Task
from satellite import Satellite
from bnb import BnB

# s_1 = Satellite(
# 	orbit="A",
# 	memory_use=10,
# 	energy_use=5,
# 	energy_gen=1,
# 	memory_storage=100,
# 	energy_storage=100,
# 	observe_time=20,
# 	downlink_time=10,
# 	uplink_time=10,
# 	sat_name="A"
# ).get()

# s_2 = Satellite(
# 	orbit="B",
# 	memory_use=10,
# 	energy_use=10,
# 	energy_gen=2,
# 	memory_storage=100,
# 	energy_storage=100,
# 	observe_time=15,
# 	downlink_time=10,
# 	uplink_time=10,
# 	sat_name="B"
# ).get()

# s_3 = Satellite(
# 	orbit="C",
# 	memory_use=20,
# 	energy_use=10,
# 	energy_gen=1,
# 	memory_storage=20,
# 	energy_storage=1,
# 	observe_time=15,
# 	downlink_time=10,
# 	uplink_time=10,
# 	sat_name="C"
# ).get()
# tasks.append(Task(1,1,50,"O",visible_at_all).get())
# tasks.append(Task(2,25,55,"O",visible_at_all).get())
# tasks.append(Task(3,30,55,"U",visible_at_all).get())
# tasks.append(Task(4,60,80,"D",visible_at_all).get())
# tasks.append(Task(5,80,100,"O",visible_at_all).get())
# tasks.append(Task(6,80,100,"O",visible_at_all).get())
# tasks.append(Task(7,100,120,"U",visible_at_all).get())
# tasks.append(Task(8,100,120,"D",visible_at_all).get())
# tasks.append(Task(9,120,150,"O",visible_at_all).get())
# tasks.append(Task(10,125,150,"O",visible_at_all).get())
# tasks.append(Task(11,130,160,"O",visible_at_all).get())
# tasks.append(Task(12,140,180,"O",visible_at_all).get())
# tasks.append(Task(13,140,180,"U",visible_at_all).get())
# tasks.append(Task(13,145,185,"O",visible_at_all).get())


s_1 = Satellite(
	orbit="A",
	memory_use=10,
	energy_use=20,
	energy_gen=1,
	memory_storage=30,
	energy_storage=200,
	observe_time=4,
	downlink_time=4,
	uplink_time=4,
	sat_name="landsat"
).get()

s_2 = Satellite(
	orbit="B",
	memory_use=20,
	energy_use=10,
	energy_gen=2,
	memory_storage=60,
	energy_storage=300,
	observe_time=2,
	downlink_time=2,
	uplink_time=2,
	sat_name="hotbird"
).get()
s_3 = Satellite(
	orbit="C",
	memory_use=20,
	energy_use=10,
	energy_gen=2,
	memory_storage=60,
	energy_storage=300,
	observe_time=2,
	downlink_time=2,
	uplink_time=2,
	sat_name="sentinel"
).get()
orbits = [s_1,s_2,s_3]

visible_at_all = []
for x in orbits:
	visible_at_all.append(x.get('orbit'))

tasks = []
tasks.append(Task(1,1,4,"O",visible_at_all,2).get())
tasks.append(Task(2,5,7,"D",visible_at_all,1).get())
tasks.append(Task(3,7,10,"O",visible_at_all,2).get())
tasks.append(Task(4,8,10,"O",visible_at_all,1).get())
tasks.append(Task(5,11,14,"U",visible_at_all,1).get())
tasks.append(Task(6,20,23,"D",visible_at_all,1).get())
tasks.append(Task(7,32,35,"O",visible_at_all,3).get())
tasks.append(Task(8,32,34,"O",visible_at_all,1).get())
tasks.append(Task(9,35,38,"U",visible_at_all,1).get())


bnb = BnB()
answers = bnb.run(tasks=tasks,satellites=orbits,max_solutions=0)
bnb.print_solutions(answers)
print("\nfinished in " + str(bnb.timer) + " s.")
