#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os

'''
Class Runner executes manager demanded actions
'''
class Runner():
	def __init__(self, config, generator, parser):
		self.config = config
		self.generator = generator
		self.parser = parser

	def schedule(self, instance_path = '', **kwargs):
		# clingo executable path
		clingo = self.config.getPath("clingo_exec")
		# encoding logic program path
		encoding = self.config.getPath("problem_encoding")
		# instances directory path
		instances = self.config.getPath("problem_instances_dir")
		# report file destination path
		tmp_file = self.config.getPath("tmp_file")
		# processing
		instance_path = instance_path if instance_path != '' else glob.glob(instances + "*instance*.lp")[0]
		print("instancja " + instance_path)

		os.system(clingo + " " + encoding + " " + instance_path + " > " + tmp_file)
		self.parser.process_file(tmp_file)
		# clean
		os.system("rm " + tmp_file)

	def generate(self, instances, **kwargs):
		for i in range(0,instances):
			self.generator.gen()

	def prune(self):
		instances = self.config.getPath("problem_instances_dir")
		for file in glob.glob(instances + "instance_*.lp"):
			print("usuwanie " + file + "...")
			os.system("rm " + file)
