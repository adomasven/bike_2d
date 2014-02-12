#!/usr/bin/env python2

from view import View
from entityfactory import *

class Scene(View):
    def __init__(self):
        super(Scene, self).__init__()

        self.sim_dt = 1000.0 / 100.0 #100 per second
        self.timeAcc = 0

        entFact = EntityFactory
        self.viewObjects.append(entFact.CreateNewPlayer())
        self.viewObjects.append(
            entFact.CreateNewLevelBlock(-200, -200, 400, 20))

    def update(self):
        updated = False
        a = self.allowUpdate()
        while a.next():
            super(Scene, self).update(self.sim_dt)
            updated = True
        return updated


    def allowUpdate(self):
        dt = self.getDt()
        if(dt > self.sim_dt*5): dt = self.sim_dt*5
        self.timeAcc += dt
        while(self.timeAcc >= self.sim_dt):
            self.timeAcc -= self.sim_dt
            yield True
        yield False
