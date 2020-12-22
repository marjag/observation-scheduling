#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os

class Runner():
	def __init__(self, config):
		self.config = config

	def run(self, **kwargs):
		# clingo executable path
		clingo = self.config.getRootDir() + self.config.getParam("clingo_exec")
		# encoding logic program path
		encoding = self.config.getRootDir() + self.config.getParam("problem_encoding")
		# instances directory path
		instances = self.config.getRootDir() + self.config.getParam("problem_instances_dir")
		# report file destination path
		report_file = self.config.getRootDir() + self.config.getParam("report_file")
		# processing
		ifile = glob.glob(instances + "*instance*.lp")[0]
		print(ifile)
		result = os.system(clingo + " " + encoding + " " + ifile)
		exit()
		pass

	def generate(self, **kwargs):

		pass