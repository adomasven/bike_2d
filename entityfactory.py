#!/usr/bin/env python2

from entity import *
from math import radians

class EntityFactory(object):
    def __init__(self, entityList):
        self.target = entityList
    
    def CreateNewPlayer(self, evtMngr, x=0, y=0, w=10, h=10):
        e = self.CreateNewCircle(x, y, w)
        e.type = PLAYER
        e.addComp(Velocity())
        e.addComp(Gravity())
        e.addComp(Contacts())
        e.addComp(Engine())
        e.addComp(Input(evtMngr))
        e.addComp(Breaks())
        e.updateFirst = ['velocity', 'engine', 'breaks']
        e.updateLast = ['contacts']
        return e

    def CreateNewLevelBlock(self,x=0, y=0, width=10, heigth=10, angle=0):
        e = self.CreateNewBox(x, y, width, heigth, angle)
        e.type = LEVEL_BLOCK
        return e

    def CreateNewCircle(self,x=0, y=0, r=10):
        e = Entity(self.target)
        e.type = CIRCLE
        e.addComp(Position(x, y))
        e.addComp(CircleModel(e.position, r))
        e.addComp(CircleHitbox(r))
        return e

    def CreateNewBox(self,x=0, y=0, width=10, heigth=10, angle=0):
        e = Entity(self.target)
        e.type = BOX
        e.addComp(Position(x, y, radians(angle)))
        e.addComp(BoxModel(e.position, width, heigth))
        e.addComp(Hitbox(width, heigth))
        return e

    def CreateNewFPSMeter(self,x=10, y=0, fontSize=32):
        e = Entity(self.target)
        e.type = HUD_FPS
        e.addComp(FPSCounter())
        e.addComp(FPSModel(e.fpscounter, Position(x, y), fontSize))
        return e