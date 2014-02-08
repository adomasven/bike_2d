#!/usr/bin/env python2

from model import *
from basecomponent import Component

class Position(Component):
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Movable(Component):
    x = 0
    y = 0

    def __init__(self, position):
        self.position = position

    def update(self, ent, dt):
        pass

class Collidable(Component):
    def update(self, ent, dt):
        pass
