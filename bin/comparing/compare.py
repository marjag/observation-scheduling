#!/usr/bin/python3
# -*- coding: utf-8 -*-

from task import Task
from satellite import Satellite
from bnb import BnB

s_1 = Satellite("A",10,5,10,10,1,20,10,10,'A').get()
s_2 = Satellite("B",20,10,10,20,1,15,10,10,'B').get()
s_3 = Satellite("C",20,10,10,20,1,15,10,10,'C').get()
visible_at_all = [s_1.get('orbit'),s_2.get('orbit')]

t_1 = Task("1",1,50,"O",visible_at_all).get()
t_2 = Task("2",25,55,"O",visible_at_all).get()
t_3 = Task("3",30,55,"U",visible_at_all).get()
t_4 = Task("4",60,80,"O",visible_at_all).get()
t_5 = Task("5",80,100,"U",visible_at_all).get()

BnB([t_1,t_2],[s_1,s_2])