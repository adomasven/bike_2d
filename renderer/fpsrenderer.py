#!/usr/bin/env python2

from fontrenderer import *
from sdl2 import *

class FPSRenderer(FontRenderer):
    def __init__(self, renderer):
        FontRenderer.__init__(self, renderer)

    def draw(self, model):
        FontRenderer.draw(self, model.surfacep.contents, model)