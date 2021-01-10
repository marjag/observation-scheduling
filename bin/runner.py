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

	def schedule(self, instance_path, **kwargs):
		# little bit more user-friendly (gets only file name, not full path)
		instance_path = instance_path.split('/')[-1]
		# clingo executable path
		clingo = self.config.getPath("clingo_exec")
		# encoding logic program path
		encoding = self.config.getPath("problem_encoding")
		# instances directory path
		instances = self.config.getPath("problem_instances_dir")
		# report file destination path
		tmp_file = self.config.getPath("tmp_file")
		# processing
		instance_path = instances + instance_path
		if os.path.isfile(instance_path) == False:
			exit("Nie ma takiego pliku: " + instance_path)

		print("instancja " + instance_path)
		os.system(clingo + " " + encoding + " " + instance_path + " > " + tmp_file)
		self.parser.process_file(tmp_file, kwargs.get('answers') or 1)
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