#!/usr/bin/env python2

from entityfactory import *
from collision import *

class Scene(object):
    def __init__(self, evtMngr):
        self.time = timer.SDL_GetTicks()
        self.sceneObjects = []
        self.hudObjects = []

        self.sim_dt = 1000.0 / 60.0 #100 per second
        self.timeAcc = 0

        entFact = EntityFactory(self.sceneObjects)

        self.player = entFact.CreateNewPlayer(evtMngr, 0, 0, 45)

        entFact.CreateNewLevelBlock(-200, -200, 400, 20)
        entFact.CreateNewLevelBlock(-300, 200, 600, 20)
        entFact.CreateNewLevelBlock(-300, -300, 600, 20, 45)
        entFact.CreateNewLevelBlock(-300, -300, 600, 20, -45)

        entFact.target = self.hudObjects
        self.hudObjects.append(
                entFact.CreateNewFPSMeter()
            )

    def update(self):
        updated = False
        a = self.allowUpdate()
        while a.next():
            self.updateObjects(self.sceneObjects, self.sim_dt)
            self.updateObjects(self.hudObjects, self.sim_dt)
            updated = True
        CollisionResolver.resolveCollisions(self.player, self.sceneObjects)

    def updateObjects(self, objects, dt=None):
        if not dt: dt = self.getDt()

        for o in objects:
            o.update(dt / 1000)


    def allowUpdate(self):
        dt = self.getDt()
        if(dt > self.sim_dt*5): dt = self.sim_dt*5
        self.timeAcc += dt
        while(self.timeAcc >= self.sim_dt):
            self.timeAcc -= self.sim_dt
            yield True
        yield False

    def getDt(self):
        newTime = timer.SDL_GetTicks()
        dt = newTime - self.time
        self.time = newTime
        return dt
