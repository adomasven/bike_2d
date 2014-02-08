#!/usr/bin/env python2

class Scene(object):

    def __init__(self, game):
        self.game = game
        self.gameObjects = []

        entFact = game.entityFactory
        self.gameObjects.append(entFact.CreateNewPlayer())
        self.gameObjects.append(
            entFact.CreateNewLevelBlock(-200, -200, 400, 20))

    def update(self, dt):
        for o in self.gameObjects:
            o.update(dt)