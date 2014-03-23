#!/usr/bin/env python2

from __future__ import division

from entityfactory import *
from collision import *

class Scene(object):
    def __init__(self, evtMngr):
        self.time = timer.SDL_GetTicks()
        self.sceneObjects = []
        self.hudObjects = []
        self.updateEntities = []

        self.sim_dt = 1.0 / 100.0 #100 per second
        self.timeAcc = 0

        entFact = EntityFactory(evtMngr, self.sceneObjects, self.updateEntities)

        self.player = entFact.CreatePlayer(0, -10, 45)

        entFact.CreateLevelBlock(-400, -210, 800, 20)
        entFact.CreateLevelBlock(-400, 280, 800, 20)
        entFact.CreateLevelBlock(-300, 180, 600, 20)
        entFact.CreateLevelBlock(-400, -20, 600, 20, -45)
        entFact.CreateLevelBlock(0, -420, 600, 20, 45)

        entFact.CreateLevelBlock(-380, -300, 600, 20, 90)
        entFact.CreateLevelBlock(400, -300, 600, 20, 90)

        entFact.drawTarget = self.hudObjects
        entFact.CreateFPSMeter()
        entFact.CreateParameterMonitor(
            lambda f: str(self.player.chassis.wheels[0].contacts.isColliding),
            y=500
            )

    def update(self):
        a = self.allowUpdate()
        while a.next():
            self.updateObjects(self.updateEntities, self.sim_dt)
            for w in self.player.chassis.wheels:
                CollisionResolver.resolveCollisions(w, self.updateEntities)

    def updateObjects(self, objects, dt=None):
        if not dt: dt = self.getDt()

        for o in objects:
            o.update(dt)


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
        return dt / 1000
