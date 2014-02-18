#!/usr/bin/env python2

from __future__ import division
from math import pi
from copy import deepcopy

from model import *
from basecomponent import Component
from sdl2 import *
from vec2d import Vec2d
from collision import BoundingBox, BoundingCircle, BoundingPolygon
from eventmanager import *

class Spring(Component):
    def __init__(self, ent1, ent2, length=100, resistence=.1):
        self.length = length
        self.resistence = resistence
        self.ent1 = ent1
        self.ent2 = ent2
        self.mConst = ent1.physprops.mass / (ent1.physprops.mass + ent2.physprops.mass)

    def update(self, ent, dt):
        ent1, ent2 = self.ent1, self.ent2
        mConst = self.mConst
        dist = (self.ent1.position - self.ent2.position)
        dist.length -= self.length
        dist.length *= self.resistence
        ent1.forces.addAcc(-dist / dt**2 * (1-mConst))
        ent2.forces.addAcc(dist / dt**2 * (mConst))

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

        for w in self.wheels:
            w.update(dt)

    def changeDirection(self):
        self.frontWheel.engine.active = not self.frontWheel.engine.active
        self.backWheel.engine.active = not self.backWheel.engine.active

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

    def __str__(self):
        string = "# " + str(id(self)) 
        string += " " + str(self.mass)
        string += " " + str(self.rotFriction)
        string += " " + str(self.grip)
        string += " " + str(self.centreOfMass)
        string += " " + str(self.restitution)
        return  string


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

    # def update(self, ent, dt):
    #     try: 
    #         ent.velocity
    #         while self.x < -400:
    #             self.x += 800
    #         while self.y < -300:
    #             self.y += 600
    #         while self.x > 400:
    #             self.x -= 800
    #         while self.y > 300:
    #             self.y -= 600
    #     except KeyError: pass

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
        copy._rps = self._rps
        return copy

    def update(self, ent, dt):
        resVec = ent.contacts.resVec
        surface = resVec.perpendicular()

        self -= self.dot(surface) * surface * ent.forces.lockCoef
        self -= self.dot(surface) * -surface * ent.forces.lockCoef
        ent.position += self * dt
        ent.position.angle += self.rps * dt * 2*pi
        if ent.contacts.isColliding:
                    ent.position += resVec * (ent.contacts.length)

        
class Forces(Vec2d, Component):
    def __init__(self, x=0, y=-500):
        Vec2d.__init__(self, x, y)
        self.accDif = 0
        self.lockCoef = 0


    def update(self, ent, dt):
        self.lockCoef = 0
        resVec = ent.contacts.resVec
        surface = resVec.perpendicular()
        try: radius = ent.hitbox.r
        except KeyError: radius = 1

        #update angular acc/speeds
        #designed to work with round objects
        angularSpeed = ent.velocity.rps * radius * 2*pi
        
        try:
            if ent.breaks.brk: 
                breakSpeed = ent.breaks.grip * ent.breaks.decc * dt
                if abs(angularSpeed) < breakSpeed:
                    angularSpeed = 0
                    self.lockCoef = ent.physprops.grip
                else:
                    angularSpeed -= breakSpeed*(angularSpeed/abs(angularSpeed))
        except AttributeError: pass
        ent.velocity.rps = (
            angularSpeed / radius /(2*pi) * (1 - ent.physprops.rotFriction)
        )

        # update directional forces/speeds
        acc = Vec2d(self) + self.accDif
        self.accDif = 0
        if ent.contacts.isColliding:
            acc -= acc.dot(resVec) * resVec * .82
            acc -= (
                ent.velocity.dot(resVec) * resVec * 
                (1 + ent.physprops.restitution) / dt
            )
        ent.velocity += acc * dt

    def addAcc(self, acc):
        self.accDif += acc

class Engine(Component):
    CW = -1
    CCW = 1
    def __init__(self, force=50):
        self.active = True
        self.acc = False
        self.rotation = Engine.CW
        self.force = force

    def update(self, ent, dt):
        if self.active:
            if self.acc:
                ent.velocity.rps +=(
                    self.force * self.rotation * dt
                )

class Breaks(Component):
    def __init__(self, decc=100000, grip=1):
        self.grip = grip
        self.decc = decc
        self.brk = False

class Contacts(Component):
    def __init__(self):
        self.colliderList = []
        self.isColliding = False
        self._resVec = Vec2d(0, 0)
        self.length = 0

    @property
    def resVec(self):
        if self._resVec == None:
            self._resVec = Vec2d(0, 0)
            for c in self.colliderList:
                self._resVec += c.resVec * c.length
            self.length = self._resVec.normalize_return_length()

        return self._resVec
    @resVec.setter
    def resVec(self, value):
        self._resVec = value
    
    def __deepcopy__(self, memo):
        copy = type(self)()
        memo[id(self)] = copy
        copy._resVec = self.resVec
        copy.colliderList = deepcopy(self.colliderList)
        copy.isColliding = self.isColliding
        copy.length = self.length
        return copy

    def update(self, ent, dt):
        self.resVec = None
        self.isColliding = False
        if self.colliderList:
            self.isColliding = True
            self.resVec #update resVecVal
            for c in self.colliderList:
                self.resolveRotation(ent, c, dt)

            self.colliderList = []

    def resolveRotation(self, ent, c, dt):
        v = ent.velocity
        surface = c.resVec.perpendicular()
        grip = ent.physprops.grip * c.other.physprops.grip
        linearAngSpeed = ent.velocity.rps * ent.hitbox.r * 2*pi

        #reaction speed
        N = abs(ent.forces.dot(c.resVec)) / dt

        #spin speed and slide speed if left any from grip
        Fspin = (linearAngSpeed - v.dot(surface)) * grip
        Fslide = (abs(Fspin) - N) * (1 - grip) if abs(Fspin) > N else 0
        if Fslide > 0: Fslide *= -Fspin/abs(Fspin)

        ent.velocity.rps += (
            (Fslide * (1-ent.physprops.restitution) - Fspin/2) /
            (ent.hitbox.r * (2*pi))
        )
        ent.forces.addAcc(Fspin / dt * surface/2)

    def add(self, collider):
        self.colliderList.append(collider)

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
            self.changeDirection = False

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