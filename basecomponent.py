#!/usr/bin/env python2


'''
Component "update" method get's called every update of the view
in which it is in.
'''
class Component(object):
    ID_COUNT = 0
    def __init__ (self, *args, **kwargs):
        self.id = Component.ID_COUNT
        Component.ID_COUNT += 1