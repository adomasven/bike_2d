#!/usr/bin/env python2

from scene import *
from renderer import Renderer
from hud import *
from collision import *
import sdl2.ext as sdl2ext
from sdl2 import *

class Game():
    
    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)

        self.scene = Scene()
        self.hud = HUD()
        self.renderer = Renderer(800, 600)

    def run(self):
        self.running = True
        while self.running:
            self.events = self.getSDLEvents()

            if(self.scene.update()):
                CollisionResolver.resolveCollisions(self.scene.viewObjects)
            self.hud.update()
            self.renderer.draw([self.scene, self.hud])

            if SDL_QUIT in self.events: self.running = False

        return 0

    def getSDLEvents(self):
        events = sdl2ext.get_events()
        newEvents = dict()
        for event in events:
            try: newEvents[event.type] += [event]
            except: newEvents[event.type] = [event]

        return newEvents