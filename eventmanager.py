#!/usr/bin/env python2

E_UPDATE_GAME = 0
E_UPDATE = 1
E_KEYDOWN = 2
E_KEYUP = 3
E_QUIT = 4
E_SDL_EVENT = 5
E_RENDER = 6

class EventManager(object):
    continueHandling = True

    def __init__():
        self.handlers = dict()
        self.queue = []
        self.urgentQueue = []

    def attachHandler(self, etype, fn):
        try: self.handlers[etype].append(fn)
        except self.handlers[etype] = [fn]

    def handleEvent(self, event):
        for fn in sel.handlers[event.type]:
            fn(event.args)

    def queueEvent(self, etype, *args, **kvargs):
        self.queue.append(Event(etype, *args, **kvargs))

    def queueUrgentEvent(self, etype, *args, **kvargs):
        self.urgentQueue.append(Event(etype, *args, **kvargs))

    def handleEvents(self):
        while continueHandling:
            handleEvent(self.queue.pop(0))
            while(urgentQueue):
                handleEvent(self.urgentQueue.pop(0))
        continueHandling = True

    def onSdlEvent(self):
        events = sdl2ext.get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    eventManager.queueEvent(E_QUIT)
                if event.type == SDL_KEYDOWN 
                    eventManager.handleEvent(Event(E_KEYDOWN, event))
                if event.type == SDL_KEYUP
                    eventManager.handleEvent(Event(E_KEYUP, event))

        self.queueEvent(E_SDL_EVENT)


class Event(object):
    def __init__(self, etype, *args, **kvargs):
        self.type = etype
        self.args = (args, kvargs)