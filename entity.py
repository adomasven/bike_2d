#!/usr/bin/env python2

from components import *

class EntityType(object):
    ENTITY = 0
    PLAYER = 1
    LEVEL_BLOCK = 2

class Entity(dict):
    def update(self, dt):
        for compType, comp in self.iteritems():
            comp.update(self, dt)
