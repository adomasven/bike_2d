#!/usr/bin/env python2

from scene import *
from renderer import Renderer
from eventmanager import *
import sdl2.ext as sdl2ext
from sdl2 import *

class Game():
    
    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)

        self.evtMngr = EventManager()
        self.scene = Scene(self.evtMngr)
        self.renderer = Renderer(self.evtMngr, 800, 600)

        self.evtMngr.attachHandler(E_SDL_EVENT, self.onSDLEvent)

    def run(self):
        self.running = True
        while self.running:
            self.queueSDLEvents()

            self.evtMngr.handleEvents()
            self.scene.update()
            self.renderer.draw(self.scene)

        return 0

    def onSDLEvent(self, eType, e):
        if eType == SDL_QUIT:
            self.running = False
        if eType == SDL_KEYDOWN and e.key.keysym.sym == SDLK_ESCAPE:
            self.running = False

    def queueSDLEvents(self):
        events = sdl2ext.get_events()
        newEvents = dict()
        for event in events:
            self.evtMngr.queueEvent(E_SDL_EVENT, event.type, event)