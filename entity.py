#!/usr/bin/env python2

from copy import deepcopy
from components import *

ENTITY = 0
PLAYER = 1
BOX = 2
CIRCLE = 3
WHEEL = 4
LEVEL_BLOCK = 10
HUD_ELEM = 100

class Entity(object):

    def __init__(self, target):
        self.updateFirst = []
        self.updateLast = []
        self.comps = dict()
        self.type = ENTITY
        try: target.append(self)
        except AttributeError: pass

    def __hash__(self): return id(self)

    def __eq__(self, other):
        return self is other

    def __getattribute__(self, name):
        try: return object.__getattribute__(self, name)
        except AttributeError:
            if len(self.comps[name]) <= 1:
                return self.comps[name][0]

    def __deepcopy__(self, memo):
        copy = type(self)(None)
        memo[id(self)] = copy
        copy.comps = deepcopy(self.comps, memo)
        return copy

    def __str__(self):
        return "Entity #" + str(id(self)) + " " + "type: " + str(self.type)

    def update(self, dt):
        for compType in self.updateFirst:
            compList = self.comps[compType]
            for c in compList:
                self.updateComponent(dt, c)

        for compType, compList in self.comps.iteritems():
            if compType not in self.updateFirst and \
               compType not in self.updateLast:
                for c in compList:
                    self.updateComponent(dt, c)

        for compType in self.updateLast:
            compList = self.comps[compType]
            for c in compList:
                self.updateComponent(dt, c)

    def updateComponent(self, dt, comp):
        try: comp.update(self, dt)
        except AttributeError as e: pass

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