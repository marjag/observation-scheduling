#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randrange

class Utils:
	def __init__(self):
		return None

	def window_time(self):
		return randrange(1,5)

	def rand_decimal(self):
		return randrange(1,9) * 10

	def rand_hundred(self):
		return self.rand_decimal() * 10

	def rand_thousand(self):	
		return self.rand_decimal() * 100

	def rand_divisible_10(self):
		return self.rand_decimal() * randrange(1, 99)

	def rand_divisible_50(self):
		return randrange(1,9) * 50 * randrange(1, 99)

