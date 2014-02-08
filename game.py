#!/usr/bin/env python2

from scene import *
from renderer import Renderer
from entityfactory import *
import sdl2.ext as sdl2ext
from sdl2 import *

FPSCAP = 60.0
SIM_DT = 1000.0 / 100.0

class Game():
    renderer = Renderer(800, 600)
    simTimeAcc = 0.0
    rendTimeAcc = 0.0
    running = True
    
    def __init__(self):
        self.entityFactory = EntityFactory(self)
        self.scene = Scene(self)
        self.currTime = SDL_GetTicks()

    def run(self):
        while self.running:
            self.events = self.getSDLEvents()

            newTime = SDL_GetTicks()
            frameTime = newTime - self.currTime
            self.currTime = newTime
            self.simTimeAcc += frameTime
            self.rendTimeAcc += frameTime

            # simulate with fixed time change
            while(self.simTimeAcc >= SIM_DT):
                self.simTimeAcc -= SIM_DT
                self.scene.update(SIM_DT)

            # render keeping fixed frames per second
            while(self.rendTimeAcc >= 1000 / FPSCAP):
                self.rendTimeAcc -= 1000/FPSCAP
                self.rendTimeAcc -= self.rendTimeAcc * FPSCAP
                self.renderer.draw(self.scene)

            if SDL_QUIT in self.events: self.running = False

        return 0

    def getSDLEvents(self):
        events = sdl2ext.get_events()
        newEvents = dict()
        for event in events:
            try: newEvents[event.type] += [event]
            except: newEvents[event.type] = [event]

        return newEvents