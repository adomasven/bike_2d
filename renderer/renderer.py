#!/usr/bin/env python2

from OpenGL.GL import *
from sdl2 import *
from model import *
from __init__ import *
from eventmanager import *

class Renderer(object):
    
    modelRenderers = {
        MODEL_BOX:'boxRenderer',
        MODEL_CIRCLE:'circleRenderer',
        MODEL_TEXT:'fontRenderer',
    }

    def __init__(self, evtMngr, winWidth=800, winHeight=600):
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.evtMngr = evtMngr
        self.time = SDL_GetTicks()
        self.timeAcc = 0
        self.limitFPS = True
        self.fpsCap = 60.0

        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3);
        SDL_GL_SetAttribute(
            SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
        self.window = SDL_CreateWindow("2d bike", 
            SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
            winWidth, winHeight, SDL_WINDOW_OPENGL
            )
        SDL_GL_CreateContext(self.window)

        glClearColor(0, 0, 0, 0)

        # needed for blending text and sprites(?)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        # SDL_GL_SetSwapInterval(0) # disable v-sync

        self.camToClipMat = self.getCamToClipMat()

        self.boxRenderer = BoxRenderer(self)
        self.fontRenderer = FontRenderer(self)
        self.circleRenderer = CircleRenderer(self)

    def getCamToClipMat(self):
        mat = identityMatrix()
        mat[0,0] = 2.0/self.winWidth
        mat[1,1] = 2.0/self.winHeight
        return mat

    def allowRendering(self):
        if not self.limitFPS: return True

        newTime = SDL_GetTicks()
        self.timeAcc += newTime - self.time
        self.time = newTime

        allow = False
        while(self.timeAcc >= 1000.0 / self.fpsCap):
            self.timeAcc -= 1000.0 / self.fpsCap
            allow = True
        return allow


    def draw(self, view):
        if self.allowRendering():
            self.evtMngr.queueEvent(E_ON_DRAW)
            self.swapBuffer()
            self.drawObjects(view.sceneObjects)
            self.drawObjects(view.hudObjects)

    def drawObjects(self, objects):
        for renderer, models in self.buildRenderingQueue(objects).iteritems():
            
            modelRenderer = getattr(self, self.modelRenderers[renderer])
            modelRenderer.drawModels(models)

    def buildRenderingQueue(self, objects):
        queue = dict()
        for o in objects:
            try: 
                try: queue[o.model.type].append(o.model)
                except: queue[o.model.type] = [o.model]
            except KeyError: pass
        return queue

    def swapBuffer(self):
        SDL_GL_SwapWindow(self.window)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)