#!/usr/bin/env python2

from components import *
from operator import attrgetter

ENTITY = 0
PLAYER = 1
BOX = 2
CIRCLE = 3
LEVEL_BLOCK = 10
HUD_FPS = 100

class Entity(dict):
    HASH_NUM = 0
    def __init__(self):
        self.updatePriority = []
        self.mass = 0
        self.hashNum = Entity.HASH_NUM
        Entity.HASH_NUM += 1

    def __hash__(self): return self.hashNum

    def __eq__(self, other):
        return self is other


    def update(self, dt):
        for compType in self.updatePriority:
            if type(self[compType]) is list:
                for c in self[compType]:
                    self.updateComponent(dt, c)
            else:
                self.updateComponent(dt, comp)

        for compType, comp in self.iteritems():
            if compType not in self.updatePriority:
                if type(comp) is list:
                    for c in comp:
                        self.updateComponent(dt, c)
                else:
                    self.updateComponent(dt, comp)
            


    def updateComponent(self, dt, comp):
        try: comp.update(self, dt)
        except AttributeError: pass