#!/usr/bin/env python2

from model import *
from basecomponent import Component
from sdl2 import timer
from vec2d import Vec2d
from collision import BoundingBox, BoundingCircle

class Position(Vec2d):
    pass

class Velocity(Vec2d):
    def __init__(self, maxV=1000000, x=0, y=0):
        super(Velocity, self).__init__(x, y)
        self.maxV = maxV

    def update(self, ent, dt):
        try: ent['position'] += self * dt
        except TypeError as e: print e

class Hitbox(Component):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def getBoundingBox(self, ent):
        pos = ent['position']
        return BoundingBox(pos.x, pos.y, self.w, self.h)

class CircleHitbox(Component):
    def __init__(self, r):
        self.r = r

    def getBoundingCircle(self, ent):
        pos = ent['position']
        return BoundingCircle(pos.x, pos.y, self.r)

class Gravity(Vec2d):
    def __init__(self, x=0, y=-500):
        super(Gravity, self).__init__(x, y)

    def update(self, ent, dt):
        try: ent['velocity'] += self * dt
        except TypeError as e: print e

class Contacts(Component):
    def __init__(self):
        self.colliders = []

    def resolveContacts(self, ent):
        for c in self.colliders:
            ent['position'] += c.minResVec
            ent['velocity'] += c.minResVec.normalized() * ent['velocity'].length * 1.5
        self.colliders = []

    def add(self, collider):
        self.colliders.append(collider)

class FPSCounter(Component):
    def __init__(self):
        self._time = timer.SDL_GetTicks()
        self.fps = 0
        self._count = 0
        self._timeToSec = 1000

    def updateCounter(self):
        newTime = timer.SDL_GetTicks()
        self._timeToSec -= newTime - self._time
        self._time = newTime
        if(self._timeToSec <= 0):
            self._timeToSec = 1000
            self.fps = self._count
            self._count = 0
        self._count += 1
        return self.fps