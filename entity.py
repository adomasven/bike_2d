#!/usr/bin/env python2

from components import *
from operator import attrgetter

ENTITY = 0
PLAYER = 1
BOX = 2
CIRCLE = 3
LEVEL_BLOCK = 10
HUD_FPS = 100

class Entity(object):
    ID_COUNT = 0

    def __init__(self):
        self.updatePriority = []
        self.id = Entity.ID_COUNT
        self.comps = dict()
        Entity.ID_COUNT += 1

    def __hash__(self): return self.id

    def __eq__(self, other):
        return self is other

    def __getattribute__(self, name):
        try: return object.__getattribute__(self, name)
        except AttributeError:
            if len(self.comps[name]) <= 1:
                return self.comps[name][0]

    def update(self, dt):
        for compType in self.updatePriority:
            for compList in self.comps[compType]:
                for c in compList:
                    self.updateComponent(dt, c)

        for compType, compList in self.comps.iteritems():
            if compType not in self.updatePriority:
                for c in compList:
                    self.updateComponent(dt, c)

    def updateComponent(self, dt, comp):
        try: comp.update(self, dt)
        except AttributeError: pass

    def addComp(self, comp, append=False, compName=None):
        if not compName:
            try: compName = comp.compName
            except AttributeError: compName = comp.__class__.__name__.lower()
        if append:
            try: self.comps[compName].apppend(comp)
            except KeyError:
                self.comps[compName] = [comp]
        else:
            self.comps[compName] = [comp]