#!/usr/bin/env python2

from entity import *
from math import radians

class EntityFactory(object):
    def __init__(self, evtMngr, drawTarget, updateTarget):
        self.drawTarget = drawTarget
        self.updateTarget = updateTarget
        self.evtMngr = evtMngr
    
    def CreatePlayer(self, x=0, y=0, w=10, h=10):
        fw = self.CreateWheel(x + 50, y)
        bw = self.CreateWheel(x - 50, y)
        bikerim = self.CreateBox(x - 15, y + 40, 30, 30, update=False)
        bikerim.addComp(Velocity())
        bikerim.addComp(Forces())
        bikerim.addComp(Contacts())
        bikerim.physprops.mass = 40
        e = Entity(self.drawTarget, self.updateTarget)
        e.type = PLAYER
        e.addComp(Input(self.evtMngr))
        # e.addComp(Spring(bikerim, fw, 80, .5), True)
        # e.addComp(Spring(bikerim, bw, 80, .5), True)
        e.addComp(Spring(fw, bw, resistence=.03, lockVel=0), True)
        e.addComp(Chassis(fw, bw))
        e.chassis.wheels += [bikerim]
        e.updateFirst += ['spring']
        return e

    def CreateLevelBlock(self,x=0, y=0, width=10, heigth=10, angle=0):
        e = self.CreateBox(x, y, width, heigth, angle)
        e.addComp(Hitbox(width, heigth))
        e.type = LEVEL_BLOCK
        return e

    def CreateWheel(self, x=0, y=0, r=20):
        e = self.CreateCircle(x, y, r)
        e.type = WHEEL
        e.addComp(Velocity())
        e.addComp(Forces())
        e.addComp(Contacts())
        e.addComp(Engine())
        e.addComp(Breaks())
        e.addComp(CircleHitbox(r))
        e.physprops.mass = 7
        e.physprops.grip = 1
        e.physprops.rotFriction = .01
        e.physprops.restitution = .1
        e.updateFirst += ['engine', 'contacts', 'forces', 'breaks', ]
        e.updateLast = ['velocity'] + e.updateLast
        return e

    def CreateCircle(self, x=0, y=0, r=10):
        e = Entity(self.drawTarget)
        e.type = CIRCLE
        e.addComp(PhysicalProperties())
        e.addComp(Position(x, y))
        e.addComp(CircleModel(e.position, r))
        e.updateLast += ['physprops']
        return e

    def CreateBox(self,x=0, y=0, w=10, h=10, angle=0, update=True):
        if update: e = Entity(self.drawTarget, self.updateTarget)
        else: e = Entity(self.drawTarget)
        e.type = BOX
        e.addComp(PhysicalProperties())#com=Vec2d(w/2, h/2)))
        e.addComp(Position(x, y, radians(angle)))
        e.addComp(BoxModel(e.position, w, h))
        e.updateLast += ['physprops']
        return e

    def CreateFPSMeter(self, x=10, y=0, fontSize=32):
        e = Entity(self.drawTarget, self.updateTarget)
        e.type = HUD_ELEM
        e.addComp(FPSCounter())
        e.addComp(
            FPSModel(self.evtMngr, Position(x, y), e.fpscounter, fontSize)
            )
        return e

    def CreateParameterMonitor(self, fn, x=10, y=550, fontSize=32):
        e = Entity(self.drawTarget, self.updateTarget)
        e.type = HUD_ELEM
        e.addComp(TextModel(self.evtMngr, Position(x, y), fontSize, fn))
        return e
