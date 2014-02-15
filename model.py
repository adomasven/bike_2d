#!/usr/bin/env python2

from basecomponent import Component
from numpy import array
from glhelpers import *
import sdl2.sdlttf as sdlttf
from sdl2.pixels import *
from sdl2.surface import *

MODEL_BOX = 0
MODEL_FPS = 1
MODEL_CIRCLE = 2

class Model(Component):
    def __init__(self, position):
        Component.__init__(self)
        self.position = position
        self.compName = "model"
    def getModelToWorldMat():
        mat = identityMatrix()
        mat[0,3] = self.position.x
        mat[1,3] = self.position.y
        return mat


class BoxModel(Model):
    def __init__(self, position, width=10, height=10):
        super(BoxModel, self).__init__(position)
        self.type = MODEL_BOX
        self.width, self.height = width, height

    def getModelToWorldMat(self):
        transScal = identityMatrix()
        transScal[0,0] = self.width
        transScal[1,1] = self.height
        transScal[0,3] = self.position.x
        transScal[1,3] = self.position.y
        rot = rotationMatrix(self.position.angle)
        return rot.dot(transScal)

class CircleModel(Model):
    def __init__(self, position, r):
        super(CircleModel, self).__init__(position)
        self.type = MODEL_CIRCLE
        self.r = r

    def getModelToWorldMat(self):
        transScal = identityMatrix()
        transScal[0,0] = self.r
        transScal[1,1] = self.r
        transScal[0,3] = self.position.x
        transScal[1,3] = self.position.y
        rot = rotationMatrix(self.position.angle)
        return transScal.dot(rot)

class FPSModel(Model):
    def __init__(self, counter, position, fontSize = 32):
        super(FPSModel, self).__init__(position)
        self.type = MODEL_FPS
        self.counter = counter
        self.currentFPS = 0
        self.colour = SDL_Colour(255, 255, 255, 255)
        self.fontFilename = "fonts/DejaVuSerif.ttf"

        if not sdlttf.TTF_WasInit():
            sdlttf.TTF_Init()

        self.ttfFont = sdlttf.TTF_OpenFont(self.fontFilename, fontSize)
        if self.ttfFont is None:
            raise TTF_GetError()

        self.surfacep = self.getFontSurface()

    def onDraw(self):
        self.counter.updateCounter()
        if(self.currentFPS != self.counter.fps):
            self.currentFPS = self.counter.fps
            self.surfacep = self.getFontSurface()

    def getFontSurface(self):
        try: SDL_FreeSurface(self.surfacep)
        except AttributeError: pass
        
        surfacep = sdlttf.TTF_RenderText_Blended(self.ttfFont, 
            str(self.currentFPS), self.colour)
        if surfacep is None:
            raise TTF_GetError()
        return surfacep

    def getModelToWorldMat(self):
        mat = identityMatrix()
        mat[0,0] = self.surfacep.contents.w
        mat[1,1] = self.surfacep.contents.h
        mat[0,3] = self.position.x + self.surfacep.contents.w
        mat[1,3] = self.position.y + self.surfacep.contents.h
        return mat
