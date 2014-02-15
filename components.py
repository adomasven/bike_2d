#!/usr/bin/env python2

from math import pi
from model import *
from basecomponent import Component
from sdl2 import *
from vec2d import Vec2d
from collision import BoundingBox, BoundingCircle, BoundingPolygon
from eventmanager import *

class Position(Vec2d, Component):
    def __init__(self, x=0, y=0, angle=0):
        Vec2d.__init__(self, x, y)
        Component.__init__(self)
        self.rads = angle

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
        Vec2d.__init__(self, x, y)
        Component.__init__(self)
        self.maxV = maxV

    def update(self, ent, dt):
        ent.position += self * dt
        if self.contacts.colliders:
            self.rads += self.length / self.hitbox.r
        

class Hitbox(Vec2d, Component):
    def getBoundingPoly(self, ent):
        pos = ent.position
        angle = pos.rads
        verts = []
        verts.append(pos.rotated(angle))
        verts.append((pos + Vec2d(0, self.y)).rotated(angle))
        verts.append((pos + self).rotated(angle))
        verts.append((pos + Vec2d(self.x, 0)).rotated(angle))
        return BoundingPolygon(verts)

class CircleHitbox(Component):
    def __init__(self, r):
        Component.__init__(self)
        self.r = r
        self.compName = 'hitbox'

    def getBoundingCircle(self, ent):
        pos = ent.position
        return BoundingCircle(pos.x, pos.y, self.r)

class Gravity(Vec2d, Component):
    def __init__(self, x=0, y=-500):
        Vec2d.__init__(self, x, y)
        Component.__init__(self)

    def update(self, ent, dt):
        ent.velocity += self * dt

class Engine(Component):
    CW = -1
    CCW = 1
    def __init__(self, power=2500):
        Component.__init__(self)
        self.active = True
        self.accelerate = False
        self.rotation = Engine.CW
        self.power = power

    def update(self, ent, dt):
        if self.active and self.accelerate and ent.contacts.colliders:
            velIncr = Vec2d(0, 0)
            for c in ent.contacts.colliders:
                direction = c.resVec.perpendicular()
                velIncr += direction
            ent.velocity += velIncr * self.rotation * self.power * dt
            ent.contacts.colliders = None

class Input(Component):
    def __init__(self, evtMngr):
        Component.__init__(self)
        self.config = {SDLK_UP:'move', SDLK_SPACE:'changeRotation'}
        self.move = False
        self.changeRotation = False
        evtMngr.attachHandler(E_SDL_EVENT, self.onSDLEvent)

    def onSDLEvent(self, eType, e):
        if eType == SDL_KEYDOWN:
            try: 
                attr = setattr(self, self.config[e.key.keysym.sym], True)
            except (AttributeError, KeyError): pass
        if eType == SDL_KEYUP:
            try: 
                attr = setattr(self, self.config[e.key.keysym.sym], False)
            except (AttributeError, KeyError): pass

    def update(self, ent, dt):
        if self.move: 
            ent.engine.accelerate = True
        else: ent.engine.accelerate = False

        if self.changeRotation:
            ent.engine.rotation *= -1
            self.changeRotation = False


class Contacts(Component):
    def __init__(self, friction=0.05, elasticity=.5):
        Component.__init__(self)
        self.colliders = None
        self.newColliders = []
        self.friction = friction
        self.elasticity = elasticity

    def resolveContacts(self, ent):
        totalResVec = Vec2d(0, 0)
        for c in self.newColliders:
            totalResVec += c.resVec * c.length

        ent.position += totalResVec
        length = totalResVec.normalize_return_length()
        ent.velocity -= totalResVec * totalResVec.dot(ent.velocity) * (
            1 + self.elasticity)
        
        ent.velocity -= self.friction * totalResVec.perpendicular() * \
                            totalResVec.perpendicular().dot(ent.velocity)
        self.colliders = self.newColliders
        self.newColliders = []

    def add(self, collider):
        self.newColliders.append(collider)

class FPSCounter(Component):
    def __init__(self):
        Component.__init__(self)
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