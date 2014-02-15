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
        self._angle = angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value % (pi * 2)

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
    def __init__(self, maxrps=21, x=0, y=0):
        Vec2d.__init__(self, x, y)
        Component.__init__(self)
        self._rps = 0
        self.maxrps = maxrps

    @property
    def rps(self):
        return self._rps
    @rps.setter
    def rps(self, value):
        if value > self.maxrps:
            self._rps = self.maxrps
        elif value < -self.maxrps:
            self._rps = -self.maxrps
        else: self._rps = value
    

    def update(self, ent, dt):
        if ent.contacts.resVec:
            rotFriction = ent.contacts.rotFriction
            slideFriction =  ent.contacts.slideFriction
            surface = ent.contacts.resVec.normalized().perpendicular()
            linearAngSpeed = self.rps * 2*pi * ent.hitbox.r

            self += surface * (linearAngSpeed - self.dot(surface)) * dt

            if ent.breaks.brk:
                self -= self.dot(surface) * slideFriction * \
                        surface * ent.breaks.strength
            else:
                self -= self.dot(surface) * rotFriction * surface

            self.rps = self.dot(surface) / (2*pi * ent.hitbox.r)

        ent.position += self * dt
        # ent.position.angle += linearAngSpeed * dt / ent.hitbox.r
        ent.position.angle += self.rps * 2*pi * dt
        

class Hitbox(Vec2d, Component):
    def getBoundingPoly(self, ent):
        pos = ent.position
        angle = pos.angle
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
    def __init__(self, power=200):
        Component.__init__(self)
        self.active = True
        self.acc = False
        self.rotation = Engine.CW
        self.power = power

    def update(self, ent, dt):
        if self.active:
            if self.acc:
                ent.velocity.rps += self.power * self.rotation * dt

class Breaks(Component):
    def __init__(self, strength=.9):
        Component.__init__(self)
        self.strength = strength
        self.brk = False

    def update(self, ent, dt):
        if self.brk:
            ent.velocity.rps /= 1 + self.strength


class Contacts(Component):
    def __init__(self, rotFriction=.001, slideFriction=1, elasticity=.5):
        Component.__init__(self)
        self.colliders = []
        self.resVec = None
        self.rotFriction = rotFriction
        self.slideFriction = slideFriction
        self.elasticity = elasticity

    def resolveContacts(self, ent):
        totalResVec = Vec2d(0, 0)
        for c in self.colliders:
            totalResVec += c.resVec * c.length

        ent.position += totalResVec
        #let it sink by one pixel
        ent.position -= totalResVec.normalized() * .2

        length = totalResVec.normalize_return_length()
        ent.velocity -= totalResVec * totalResVec.dot(ent.velocity) * (
            1 + self.elasticity)
        
        self.resVec = totalResVec * length
        self.colliders = []

    def add(self, collider):
        self.colliders.append(collider)

    def update(self, ent, dt):
        self.resVec = None

class Input(Component):
    def __init__(self, evtMngr):
        Component.__init__(self)
        self.config = {
            SDLK_UP:'acc', 
            SDLK_SPACE:'changeRotation',
            SDLK_DOWN:'brk',
            }
        self.acc = False
        self.changeRotation = False
        self.brk = False
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
        if self.acc: ent.engine.acc = True
        else:        ent.engine.acc = False

        if self.changeRotation:
            ent.engine.rotation *= -1
            self.changeRotation = False

        if self.brk: ent.breaks.brk = True
        else:        ent.breaks.brk = False



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