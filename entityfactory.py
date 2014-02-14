#!/usr/bin/env python2

from entity import *
from math import radians

class EntityFactory(object):
    
    @staticmethod
    def CreateNewPlayer(evtMngr, x=0, y=0, w=10, h=10):
        e = EntityFactory.CreateNewCircle(x, y, w)
        e.type = PLAYER
        e.addComp(Velocity())
        e.addComp(Gravity())
        e.addComp(Contacts())
        e.addComp(Engine())
        e.addComp(Input(evtMngr))
        return e

    @staticmethod
    def CreateNewLevelBlock(x=0, y=0, width=10, heigth=10, angle=0):
        e = EntityFactory.CreateNewBox(x, y, width, heigth, angle)
        e.type = LEVEL_BLOCK
        return e

    @staticmethod
    def CreateNewCircle(x=0, y=0, r=10):
        e = Entity()
        e.type = CIRCLE
        e.addComp(Position(x, y))
        e.addComp(CircleModel(e.position, r))
        e.addComp(CircleHitbox(r))
        return e

    @staticmethod
    def CreateNewBox(x=0, y=0, width=10, heigth=10, angle=0):
        e = Entity()
        e.type = BOX
        e.addComp(Position(x, y, radians(angle)))
        e.addComp(BoxModel(e.position, width, heigth))
        e.addComp(Hitbox(width, heigth))
        return e

    @staticmethod
    def CreateNewFPSMeter(x=10, y=0, fontSize=32):
        e = Entity()
        e.type = HUD_FPS
        e.addComp(FPSCounter())
        e.addComp(FPSModel(e.fpscounter, Position(x, y), fontSize))
        return e