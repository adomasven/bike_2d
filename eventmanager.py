#!/usr/bin/env python2

E_SDL_EVENT = 0

class EventManager(object):
    continueHandling = True

    def __init__(self):
        self.handlers = dict()
        self.queue = []

    def attachHandler(self, etype, fn):
        try: self.handlers[etype].append(fn)
        except: self.handlers[etype] = [fn]

    def handleEvent(self, event):
        for fn in self.handlers[event.type]:
            fn(*event.args, **event.kwargs)

    def queueEvent(self, etype, *args, **kvargs):
        self.queue.append(Event(etype, *args, **kvargs))

    def handleEvents(self):
        while self.queue:
            self.handleEvent(self.queue.pop(0))


class Event(object):
    def __init__(self, etype, *args, **kwargs):
        self.type = etype
        self.args = args
        self.kwargs = kwargs