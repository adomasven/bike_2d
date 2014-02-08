#!/usr/bin/env python2

from OpenGL.GL import *
from numpy import matrix, array
from OpenGL.arrays import vbo #wrapper for vertex buffer objects
from OpenGL.GL import shaders #convenience lib for working with shaders
from sdl2 import *
from glhelpers import *
from model import *

class Renderer(object):

    modelRenderers = {MODEL_BOX:'boxRenderer'}

    def __init__(self, winWidth=800, winHeight=600):
        self.winWidth = winWidth
        self.winHeight = winHeight
        SDL_Init(SDL_INIT_VIDEO)
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

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        # SDL_GL_SetSwapInterval(0) # disable v-sync

        self.camToClipMat = self.getCamToClipMat()

        self.boxRenderer = BoxRenderer(self.camToClipMat)

    def getCamToClipMat(self):
        mat = identityMatrix()
        mat[0,0] = 2.0/self.winWidth
        mat[1,1] = 2.0/self.winHeight
        return mat

    def draw(self, scene):
        self.swapBuffer()
        for renderer, models in self.buildRenderingQueue(scene).iteritems():
            modelRenderer = getattr(self, self.modelRenderers[renderer])
            return modelRenderer.drawModels(models)

    def buildRenderingQueue(self, scene):
        queue = dict()
        for o in scene.gameObjects:
            try: 
                try: queue[o['model'].type].append(o['model'])
                except: queue[o['model'].type] = [o['model']]
            except: pass

        return queue

    def swapBuffer(self):
        SDL_GL_SwapWindow(self.window)
        glClear(GL_COLOR_BUFFER_BIT)


class BoxRenderer():

    description = array([
         #coordinates
        -1, -1, 0,
        -1,  1, 0,
         1,  1, 0,
         1, -1, 0,
         #colours
         1, 1, 1, 1,
         1, 1, 1, 1,
         1, 1, 1, 1,
         1, 1, 1, 1,
        ], 'f4')

    indices = array([
        0, 1, 2,
        0, 2, 3
        ], 'u2')

    def __init__(self, camToClipMat):
        self.camToClipMat = camToClipMat

        self.program = compileProgram(
            "shaders/boxvs.glsl", "shaders/boxfs.glsl")

        with self.program:
            self.descrBuff = vbo.VBO(self.description)
            self.idxBuff = vbo.VBO(self.indices, 
                target="GL_ELEMENT_ARRAY_BUFFER")

            self.modelToCamMatUnif = glGetUniformLocation(
                self.program, "modelToCamMat")
            self.camToClipMatUnif = glGetUniformLocation(
                self.program, "camToClipMat")
            glUniformMatrix4fv(self.camToClipMatUnif, 1, True, camToClipMat)
            
            self.vao = VAO()
            
            with self.vao:
                self.descrBuff.bind()
                glEnableVertexAttribArray(0)
                glEnableVertexAttribArray(1)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 
                    self.descrBuff)
                glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 
                    self.descrBuff+3*4*4)

                self.idxBuff.bind()

    def draw(self, matrix):
        glUniformMatrix4fv(self.modelToCamMatUnif, 1, True, matrix)
        glDrawElements(GL_TRIANGLES, len(self.indices), 
            GL_UNSIGNED_SHORT, self.idxBuff)

    def drawModels(self, models):
        with self.program:
            with self.vao:
                for m in models:
                    self.draw(m.modelToWorldMat)




def compileProgram(vertShaderFile, fragShaderFile):
    with open(vertShaderFile) as f:
        try:
            vertShader = shaders.compileShader(f.read(), GL_VERTEX_SHADER)
        except RuntimeError as e:
            e.args += ("in file : %s"%(vertShaderFile),)
            raise

    with open(fragShaderFile) as f:
        try:
            fragShader = shaders.compileShader(f.read(), GL_FRAGMENT_SHADER)
        except RuntimeError as e:
            e.args += ("in file : %s"%(fragShaderFile),)
            raise

    return shaders.compileProgram(vertShader, fragShader)

