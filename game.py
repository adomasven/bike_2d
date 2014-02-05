#!/usr/bin/env python2

from level import *
from player import *
from renderer import Renderer
import sdl2.ext as sdl2ext
from sdl2 import *

class Game():
    renderer = Renderer(800, 600)
    
    def __init__(self):
        self.level = Level(self)
        self.player = Player(self)

    def run(self):
        running = True

        while running:
            events = sdl2ext.get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                    break
            self.renderer.swapBuffer()
            self.level.draw()
            self.player.draw()
        return 0