#!/usr/bin/env python2

from view import View

class HUD(View):

    def __init__(self, game):
        super(HUD, self).__init__(game)
        
        entFact = game.entityFactory
        self.viewObjects.append(
                entFact.CreateNewFPSMeter()
            )
