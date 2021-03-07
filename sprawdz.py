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

json_file = 'instance22.json'
print(json_file)

observations = 0
uplinks = 0
downlinks = 0
emergency = 0
visibility = 0
window= 0
priority = 0
with open(json_file) as f:
    duration = 0
    tasks = load(f).get('tasks')
    for task in tasks:
        if task.get('task_type') == 'O':
            observations += 1
        elif task.get('task_type') == 'U':
            uplinks += 1
        elif task.get('task_type') == 'D':
            downlinks += 1
        if task.get('emergency') == True:
            emergency += 1

        visibilities = task.get('visible_at')
        duration = task.get('w_end') - task.get('w_start')
        visibility += len(visibilities)
        window += duration
        priority += task.get('priority') or 0

print({"o": observations})
print({"u": uplinks})
print({"d": downlinks})
print({"e": emergency})
print({"v": visibility})
print({"w": window})
print({"w": window})
print({"p": priority})
