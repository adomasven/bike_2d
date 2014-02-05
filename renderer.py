#!/usr/bin/env python2

from OpenGL.GL import *
from numpy import matrix, array
from OpenGL.arrays import vbo #wrapper for vertex buffer objects
from OpenGL.GL import shaders #convenience lib for working with shaders
from sdl2 import *
from gl_helpers.vao import *

class Renderer():

    entityRenderers = {'box':'boxRenderer'}

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

        self.worldToCamMat = self.getWorldToCamMat()

        self.boxRenderer = BoxRenderer(self.worldToCamMat)

    def getWorldToCamMat(self):
        mat = matrix([[0]*4]*4, 'f4')
        mat[0,0] = 1.0/self.winWidth
        mat[1,1] = 1.0/self.winHeight
        mat[3,3] = 1
        return mat

    def draw(self, entity):
        entRenderer =  getattr(self, self.entityRenderers[entity.type])
        return entRenderer.draw(entity.modelToWorldMat)

    def swapBuffer(self):
        SDL_GL_SwapWindow(self.window)
        glClear(GL_COLOR_BUFFER_BIT)


class BoxRenderer():

    description = array([
         #coordinates
        -1, -1, 0, 1,
        -1,  1, 0, 1,
         1,  1, 0, 1,
         1, -1, 0, 1,
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

    def __init__(self, worldToCamMat):
        self.worldToCamMat = worldToCamMat

        self.program = compileProgram(
            "shaders/boxvs.glsl", "shaders/boxfs.glsl")

        with self.program:
            self.descrBuff = vbo.VBO(self.description)
            self.idxBuff = vbo.VBO(self.indices, 
                target="GL_ELEMENT_ARRAY_BUFFER")

            self.modelToWorldMatUnif = glGetUniformLocation(
                self.program, "modelToWorldMat")
            self.worldToCamMatUnif = glGetUniformLocation(
                self.program, "worldToCamMat")
            glUniformMatrix4fv(self.worldToCamMatUnif, 1, True, worldToCamMat)
            
            self.vao = VAO()
            
            with self.vao:
                self.descrBuff.bind()
                glEnableVertexAttribArray(0)
                glEnableVertexAttribArray(1)
                glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, 
                    self.descrBuff)
                glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 
                    self.descrBuff+4*4*4)

                self.idxBuff.bind()

    def draw(self, matrix):
        with self.program:
            glUniformMatrix4fv(self.modelToWorldMatUnif, 1, True, matrix)
            with self.vao:
                glDrawElements(GL_TRIANGLES, len(self.indices), 
                    GL_UNSIGNED_SHORT, 0)


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

