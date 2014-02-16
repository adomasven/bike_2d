#!/usr/bin/env python2

from __future__ import division
from math import pi

from model import *
from basecomponent import Component
from sdl2 import *
from vec2d import Vec2d
from collision import BoundingBox, BoundingCircle, BoundingPolygon
from eventmanager import *

class Spring(Component):
    def __init__(self, ent1, ent2, length=100, resistence=1):
        self.length = length
        self.resistence = resistence
        self.ent1 = ent1
        self.ent2 = ent2

    def update(self, ent, dt):
        dist = (self.ent1.position - self.ent2.position)
        dist.length -= self.length
        self.ent1.position += dist * self.resistence
        self.ent2.position -= dist * self.resistence
        self.ent1.velocity += dist * self.resistence / dt
        self.ent2.velocity -= dist * self.resistence / dt

class Chassis(Component):
    def __init__(self, frontWheel, backWheel, backDrive=True):
        self.frontWheel = frontWheel
        self.backWheel = backWheel
        self.wheels = [frontWheel, backWheel]
        self.acc = False
        self.brk = False
        rot = Engine.CW if backDrive else Engine.CCW
        self.frontWheel.engine.active = not backDrive
        self.backWheel.engine.active = backDrive
        self.frontWheel.engine.rotation = -rot
        self.backWheel.engine.rotation = rot

    def update(self, ent, dt):
        self.frontWheel.engine.acc = self.acc
        self.backWheel.engine.acc = self.acc
        self.frontWheel.breaks.brk = self.brk
        self.backWheel.breaks.brk = self.brk
        self.frontWheel.update(dt)
        self.backWheel.update(dt)

    def changeDir(self):
        self.frontWheel.engine.active = not self.frontWheel.engine.active
        self.backWheel.engine.active = not self.backWheel.engine.active
        self.frontWheel.engine.rotation = -self.frontWheel.engine.rotation
        self.backWheel.engine.rotation = -self.backWheel.engine.rotation

class PhysicalProperties(Component):
    def __init__(
        self, 
        mass=0, 
        rotFriction=1, 
        grip=1, 
        restitution=0.5,
        centreOfMass=Vec2d(0, 0)
        ):
        Component.__init__(self)
        self.compName = 'physprops'
        self.mass = mass
        self.rotFriction = rotFriction
        self.grip = grip
        self.centreOfMass = centreOfMass
        self.restitution = restitution


class Position(Vec2d, Component):
    def __init__(self, x=0, y=0, angle=0):
        Vec2d.__init__(self, x, y)
        self._angle = angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value % (pi * 2)

    def __deepcopy__(self, memo):
        copy = type(self)(self.x, self.y, self.angle)
        memo[id(self)] = copy
        return copy

    def update(self, ent, dt):
        try: 
            ent.velocity
            while self.x < -400:
                self.x += 800
            while self.y < -300:
                self.y += 600
            while self.x > 400:
                self.x -= 800
            while self.y > 300:
                self.y -= 600
        except KeyError: pass


class Velocity(Vec2d, Component):
    def __init__(self, x=0, y=0, maxrps=21):
        Vec2d.__init__(self, x, y)
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
    
    def __deepcopy__(self, memo):
        copy = type(self)(self.x, self.y, self.maxrps)
        memo[id(self)] = copy
        return copy

    def update(self, ent, dt):
        ent.position += self * dt
        ent.position.angle += self.rps * 2*pi * dt
        
class Gravity(Vec2d, Component):
    def __init__(self, x=0, y=-500):
        Vec2d.__init__(self, x, y)

    def update(self, ent, dt):
        ent.velocity += self * dt

class Engine(Component):
    CW = -1
    CCW = 1
    def __init__(self, power=200):
        self.active = True
        self.acc = False
        self.rotation = Engine.CW
        self.power = power

    def update(self, ent, dt):
        if self.active:
            if self.acc:
                ent.velocity.rps += self.power / ent.physprops.mass * dt * \
                                    self.rotation

class Breaks(Component):
    def __init__(self, strength=1):
        self.strength = strength
        self.brk = False

    def update(self, ent, dt):
        if self.brk:
            ent.velocity.rps -= ent.velocity.rps * self.strength

class Contacts(Component):
    def __init__(self):
        self.colliders = []
        self.rotFriction = 1
        self.resVec = " "

    def resolveContacts(self, ent):
        self.resVec = " "
        vList = []
        rpsList = []
        for c in self.colliders:
            v, rps = \
                self.onCollision(ent, c, Vec2d(ent.velocity), ent.velocity.rps)
            vList.append(v)
            rpsList.append(rps)
            self.resVec = "collision"
        ent.velocity.set(sum(vList)/len(vList))
        ent.velocity.rps = sum(rpsList)/len(rpsList)
        self.colliders = []

    def onCollision(self, ent, collision, v, rps, dt=1/60):
        c = collision
        other = c.other
        surface = c.resVec.perpendicular()
        rotFriction = ent.physprops.rotFriction * other.physprops.rotFriction
        grip = ent.physprops.grip*other.physprops.grip
        restitution = ent.physprops.restitution
        rps *= (1 - rotFriction)
        linearAngSpeed = rps * 2*pi * ent.hitbox.r

        #cancel sinking correction if breaking.
        try: 
            if v.length <= ent.gravity.length * dt*5 and ent.breaks.brk: 
                v.length = v.length * (1 - grip)
        except AttributeError: pass
        #reaction force
        N = c.resVec.dot(v)
        #bounceback
        v -= c.resVec * N * (1 + restitution)
        ent.position += c.resVec * c.length - c.resVec * 8 * dt

        #Spin force and slide friction force if left any from grip
        Fspin = (linearAngSpeed - v.dot(surface)) / 2 * grip
        Fslide = abs(N) - abs(Fspin) if abs(Fspin) > abs(N) else 0
        Fslide *= (1 - grip)

        #breaking applied fully, regardless of restitution
        try:
            if ent.breaks.brk:
                restitution = 0
        except AttributeError: pass

        #Apply acceleration.
        v += surface * (Fspin + Fslide)  * (1 - restitution)
        rps -= (Fspin - abs(Fslide)) / (ent.hitbox.r * 2*pi) *\
                 (1 - restitution)

        return v, rps


    def add(self, collider):
        self.colliders.append(collider)

    def update(self, ent, dt):
        self.rotFrict = 1
        self.resVec = " "

class Hitbox(Vec2d, Component):
    def getBoundingPoly(self, ent):
        pos = ent.position
        angle = pos.angle
        verts = []
        verts.append(pos)
        verts.append((pos + Vec2d(0, self.y).rotated(angle)))
        verts.append((pos + self.rotated(angle)))
        verts.append((pos + Vec2d(self.x, 0).rotated(angle)))
        return BoundingPolygon(verts)

class CircleHitbox(Component):
    def __init__(self, r):
        self.r = r
        self.compName = 'hitbox'

    def getBoundingCircle(self, ent):
        pos = ent.position
        return BoundingCircle(pos.x, pos.y, self.r)

class Input(Component):
    def __init__(self, evtMngr):
        self.config = {
            SDLK_UP:'acc', 
            SDLK_SPACE:'changeDirection',
            SDLK_DOWN:'brk',
            }
        self.acc = False
        self.changeDirection = False
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
        if self.acc: ent.chassis.acc = True
        else:        ent.chassis.acc = False

        if self.changeDirection:
            ent.chassis.changeDirection()

        if self.brk: ent.chassis.brk = True
        else:        ent.chassis.brk = False



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