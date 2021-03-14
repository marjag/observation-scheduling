#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from bin.config import Config
from bin.runner import Runner
from bin.generating.generator import Generator
from bin.generating.utils import Utils
from bin.parser import Parser

# input arguments
action = ''
option0 = ''
option1 = ''
option2 = ''

if len(sys.argv) > 4:
	option2 = sys.argv[4]
if len(sys.argv) > 3:
	option1 = sys.argv[3]
if len(sys.argv) > 2:
	option0 = sys.argv[2]
if len(sys.argv) > 1:
	action = sys.argv[1]

# find and remember the root path of the app
root_dir = os.path.dirname(os.path.realpath(__file__))
# working dir is set to root path of the app
os.chdir(root_dir)
config = Config(root_dir)

# instantiate runner
runner = Runner(config, Generator(config, Utils()), Parser())

if (action == 'gen'):
	if option0 == '':
		cnt = 1
	else:
		cnt = int(option0)

	print("generowanie " + str(cnt) + " instancji...")
	runner.generate(cnt)

elif action == "schedule":
	if option0 == '':
		exit("Podaj plik instancji problemu do harmonogramowania")
	print("harmonogramowanie...")
	runner.schedule(option0, answers=option1)

elif action == "prune":
	runner.prune()

else:
	print ('''Manager harmonogramowania obserwacji satelitarnych:

	python3 manager.py gen [n] - generuje n losowych instancji (domyślnie 1)
	python3 manager.py schedule <p> [m] - optymalny harmonogram dla instancji (pliku) *p*, *m* najlepszych modeli
	python3 manager.py prune - usuwa wygenerowane instancje
	python3 manager.py help - pomoc

	<a> - argument wymagany
	[a] - argument nie jest wymagany
	''')
