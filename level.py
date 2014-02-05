#!/usr/bin/env python2

from box import *

class Level():
    blocks = []

    def __init__(self, game):
        self.blocks.append(Box(-200, -200, 400, 20))
        self.game = game

    def draw(self):
        for b in self.blocks:
            b.draw(self.game.renderer)