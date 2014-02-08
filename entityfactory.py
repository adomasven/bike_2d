#!/usr/bin/env python2

from entity import *

class EntityFactory(object):
    def __init__(self, game):
        self.game = game    

    def CreateNewPlayer(self, x=0, y=0):
        e = Entity()
        e.type = EntityType.PLAYER
        e['position'] = Position(x, y)
        e['movable'] = Movable(e['position'])
        e['model'] = BoxModel(x, y)
        return e


    def CreateNewLevelBlock(self, x=0, y=0, width=10, heigth=10):
        e = Entity()
        e.type = EntityType.LEVEL_BLOCK
        e['position'] = Position(x, y)
        e['model'] = BoxModel(x, y, width, heigth)
        return e
