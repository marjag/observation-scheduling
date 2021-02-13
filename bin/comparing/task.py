#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy
'''
Class Task
'''
class Task:
	def __init__(self,task_id,w_start,w_end,task_type,visible_at,priority=0,emergency=False):
		self.task_id = task_id
		self.w_start = w_start
		self.w_end = w_end
		self.task_type = task_type
		self.visible_at = visible_at
		self.priority = priority
		self.assigned_to = []
		self.cardinality_min = 1
		self.cardinality_max = 1
		self.emergency = emergency
		if task_type != 'O':
			self.cardinality_max = 99999

	def get(self):
		o = {}
		o['task_id'] = self.task_id
		o['w_start'] = self.w_start
		o['w_end'] = self.w_end
		o['task_type'] = self.task_type
		o['visible_at'] = self.visible_at
		o['priority'] = self.priority
		o['assigned_to'] = self.assigned_to
		o['cardinality_min'] = self.cardinality_min
		o['cardinality_max'] = self.cardinality_max
		o['emergency'] = self.emergency
		return o