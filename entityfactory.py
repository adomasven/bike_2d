#!/usr/bin/env python2

from entity import *
from math import radians

class EntityFactory(object):
    
    @staticmethod
    def CreateNewPlayer(evtMngr, x=-200, y=0, w=10, h=10):
        e = EntityFactory.CreateNewCircle(x, y, w)
        e.type = PLAYER
        e['velocity'] = Velocity()
        e['gravity'] = Gravity()
        e['contacts'] = Contacts()
        e['engine'] = Engine()
        e['input'] = Input(evtMngr)
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
        e['position'] = Position(x, y)
        e['model'] = CircleModel(e['position'], r)
        e['hitbox'] = CircleHitbox(r)
        return e

    @staticmethod
    def CreateNewBox(x=0, y=0, width=10, heigth=10, angle=0):
        e = Entity()
        e.type = BOX
        e['position'] = Position(x, y, radians(angle))
        e['model'] = BoxModel(e['position'], width, heigth)
        e['hitbox'] = Hitbox(width, heigth)
        return e

    @staticmethod
    def CreateNewFPSMeter(x=10, y=0, fontSize=32):
        e = Entity()
        e.type = HUD_FPS
        e['FPSCounter'] = FPSCounter()
        e['model'] = FPSModel(e['FPSCounter'], Position(x, y), fontSize)
        return e