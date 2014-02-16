#!/usr/bin/env python2

from basecomponent import Component
from numpy import array
from glhelpers import *
import sdl2.sdlttf as sdlttf
from sdl2.pixels import *
from sdl2.surface import *
from eventmanager import *

MODEL_BOX = 0
MODEL_TEXT = 1
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
        trans = identityMatrix()
        scale = identityMatrix()
        scale[0,0] = self.width
        scale[1,1] = self.height
        trans[0,3] = self.position.x
        trans[1,3] = self.position.y
        rot = rotationMatrix(self.position.angle)
        return trans.dot(rot.dot(scale))

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

class TextModel(Model):
    def __init__(self, evtMngr, position, fontSize=32, fn=None):
        Model.__init__(self, position)
        self.type = MODEL_TEXT
        self.colour = SDL_Colour(255, 255, 255, 255)
        self.fontFilename = "fonts/DejaVuSerif.ttf"
        self.text = " "
        self.fn = fn
        evtMngr.attachHandler(E_ON_DRAW, self.onDraw)

        if not sdlttf.TTF_WasInit():
            sdlttf.TTF_Init()

        self.ttfFont = sdlttf.TTF_OpenFont(self.fontFilename, fontSize)
        try: self.ttfFont.contents
        except: raise Exception(sdlttf.TTF_GetError())

        self.surfacep = self.getFontSurface()

    def getModelToWorldMat(self):
        mat = identityMatrix()
        mat[0,0] = self.surfacep.contents.w
        mat[1,1] = self.surfacep.contents.h
        mat[0,3] = self.position.x
        mat[1,3] = self.position.y
        return mat

    def getFontSurface(self):
        try: SDL_FreeSurface(self.surfacep)
        except AttributeError: pass
        
        surfacep = sdlttf.TTF_RenderText_Blended(self.ttfFont, 
            self.text, self.colour)
        try: surfacep.contents
        except: raise Exception(sdlttf.TTF_GetError())
        return surfacep

    def onDraw(self):
        try: self.text = self.fn(None)
        except: self.text = " "
        self.surfacep = self.getFontSurface()

class FPSModel(TextModel):
    def __init__(self, evtMngr, position, counter, fontSize=32):
        self.counter = counter
        self.currentFPS = 0
        TextModel.__init__(self, evtMngr, position, fontSize)

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
        try: surfacep.contents
        except: raise Exception(sdlttf.TTF_GetError())
        return surfacep