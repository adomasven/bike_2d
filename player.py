#!/usr/bin/env python2

from box import *

class Player:

    def __init__(self, game):
        self.model = Box()
        self.game = game

    def draw(self):
        self.model.draw(self.game.renderer)