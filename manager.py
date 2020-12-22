#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from bin.config import Config
from bin.runner import Runner

root_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(root_dir)

c = Config(root_dir)
print(c)
# exit()
runner = Runner(c)
print(runner.run(mode="raw"))
