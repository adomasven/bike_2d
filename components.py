#!/usr/bin/env python2

from model import *
from basecomponent import Component
from sdl2 import *
from vec2d import Vec2d
from collision import BoundingBox, BoundingCircle
from eventmanager import *

class Position(Vec2d, Component):
    def __init__(self, x=0, y=0, angle=0):
        super(Position, self).__init__(x, y)
        self.angle = angle

    def update(self, ent, dt):
        while self.x < -400:
            self.x += 800
        while self.y < -300:
            self.y += 600
        while self.x > 400:
            self.x -= 800
        while self.y > 300:
            self.y -= 600

class Velocity(Vec2d, Component):
    def __init__(self, maxV=1000000, x=0, y=0):
        super(Velocity, self).__init__(x, y)
        self.maxV = maxV

    def update(self, ent, dt):
        try: ent['position'] += self * dt
        except TypeError as e: print e

class Hitbox(Component):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def getBoundingPoly(self, ent):
        pos = ent['position']
        verts = []
        verts.append(self.pos)
        verts.append(self.pos + Vec2d(0, self.dim.y))
        verts.append(self.pos + self.dim)
        verts.append(self.pos + Vec2d(self.dim.x, 0))
        return BoundingPolygon(verts)

class CircleHitbox(Component):
    def __init__(self, r):
        self.r = r

    def getBoundingCircle(self, ent):
        pos = ent['position']
        return BoundingCircle(pos.x, pos.y, self.r)

class Gravity(Vec2d, Component):
    def __init__(self, x=0, y=-500):
        super(Gravity, self).__init__(x, y)

    def update(self, ent, dt):
        try: ent['velocity'] += self * dt
        except TypeError as e: print e

class Engine(Component):
    CW = 1
    CCW = -1
    def __init__(self):
        self.active = True
        self.accelerate = False
        self.rotation = Engine.CW

    def update(self, ent, dt):
        if self.active and self.accelerate:
            ent['velocity'] += Vec2d(5, 0) * self.rotation

class Input(Component):
    def __init__(self, evtMngr):
        self.config = {SDLK_UP:'move', SDLK_SPACE:'changeRotation'}
        self.move = False
        self.changeRotation = False
        evtMngr.attachHandler(E_SDL_EVENT, self.onSDLEvent)

    def onSDLEvent(self, eType, e):
        if eType == SDL_KEYDOWN:
            try: 
                attr = setattr(self, self.config[e.key.keysym.sym], True)
            except: pass
        if eType == SDL_KEYUP:
            try: 
                attr = setattr(self, self.config[e.key.keysym.sym], False)
            except: pass

    def update(self, ent, dt):
        if self.move: 
            ent['engine'].accelerate = True
        else: ent['engine'].accelerate = False

        if self.changeRotation:
            ent['engine'].rotation *= -1
            self.changeRotation = False


class Contacts(Component):
    def __init__(self):
        self.colliders = []

    def resolveContacts(self, ent):
        for c in self.colliders:
            minResVec = c.minResVec
            veclen = minResVec.normalize_return_length()
            ent['position'] += c.minResVec * veclen
            ent['velocity'] -= 1.5 * minResVec * minResVec.dot(ent['velocity'])
            ent['velocity'] -= 0.01 * minResVec.perpendicular() * \
                                minResVec.perpendicular().dot(ent['velocity'])
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