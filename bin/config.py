#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

'''
Class Config holds app configuration
with cooperation with settings.json
'''
class Config:
	def __init__(self, root_dir, **kwargs):
		self.root_dir = root_dir
		self.data = {}
		self._read()

	def _read(self):
		try:
		    fname = "bin/settings.json"
		    with open(fname, 'r') as file:
		        content = file.read().replace('\n', '')
		        self.data = json.loads(content)

		except FileNotFoundError:
		    print("File {name} not found".format(name=fname))

		return None

	def getRootDir(self):
		return self.root_dir
	
	def getPath(self,to):
		return self.root_dir + self.getParam('paths').get(to)

	def getParam(self, key):
		return self.data.get(key)

	def setParam(self, key, val):
		self.data['key'] = val