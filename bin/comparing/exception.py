#!/usr/bin/python3
# -*- coding: utf-8 -*-

class DeadBranchException(Exception):
	def __init__(self,message,task=None,assignment=[]):
		self.message = message
		self.task = task 
		self.assignment = assignment
		super().__init__(self.message)

class InvalidSolutionException(Exception):
	pass