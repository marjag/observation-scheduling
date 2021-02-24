#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bin.comparing.task import Task
from bin.comparing.satellite import Satellite
from bin.comparing.bnb import BnB
from operator import itemgetter
from json import loads
from json import load
from bin.config import Config
import os

# find and remember the root path of the app
root_dir = os.path.dirname(os.path.realpath(__file__))
# working dir is set to root path of the app
os.chdir(root_dir)
config = Config(root_dir)
problems_path = config.getPath('compare_instances_json')

problems = []
with open(problems_path) as f:
	problems = load(f).get('problems')

bnb = BnB()
for problem in problems:
	tasks = problem.get('tasks')
	orbits = problem.get('orbits')
	# tasks = tasks[:15]
	solutions = bnb.run(tasks=tasks,satellites=orbits,max_solutions=1)
	print("\n\nharmonogramowanie dla branch & bound...")
	bnb.print_solutions(solutions)
	print("\nwykonano w " + str(bnb.timer) + " s.")
