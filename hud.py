#!/usr/bin/env python2

from view import View
from entityfactory import *

class HUD(View):

    def __init__(self):
        super(HUD, self).__init__()
        self.lastUpdateTime = self.time
        
        entFact = EntityFactory
        self.viewObjects.append(
                entFact.CreateNewFPSMeter()
            )

    def update(self):
        #updates self.time
        dt = self.getDt()
        if(self.time > self.lastUpdateTime + 1000.0 / 60):
            super(HUD, self).update(self.lastUpdateTime - self.time)
            self.lastUpdateTime = self.time
