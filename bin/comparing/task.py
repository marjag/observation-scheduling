#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Class Task
'''
class Task:
	def __init__(self,task_id,w_start,w_end,task_type,visible_at,priority=1):
		self.task_id = task_id
		self.w_start = w_start
		self.w_end = w_end
		self.task_type = task_type
		self.visible_at = visible_at
		self.priority = priority
		self.assigned_to = []

	def get_task_id(self):
		return self.task_id

	def get_w_start(self):
		return self.w_start

	def get_w_end(self):
		return self.w_end

	def get_task_type(self):
		return self.task_type

	def get_priority(self):
		return self.priority

	def is_visible_at(self,orbit):
		return orbit in self.visible_at

	def assign(self,satellite):
		self.assigned_to = satellite

	def is_assigned(self):
		return len(self.assigned_to) > 0

	def get_assigned_to(self):
		return self.assigned_to;

	def serialize(self):
		o = {}
		o["task_id"] = self.task_id
		o["w_start"] = self.w_start
		o["w_end"] = self.w_end
		o["task_type"] = self.task_type
		o["visible_at"] = self.visible_at
		o["priority"] = self.priority
		o["orbits"] = self.assigned_to
		return o