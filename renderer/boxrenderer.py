#!/usr/bin/env python2

from modelrenderer import *
from numpy import array
from sdl2 import *
from OpenGL.GL import *
from OpenGL.arrays import vbo #wrapper for vertex buffer objects
from glhelpers import *

class BoxRenderer(ModelRenderer):

    vertexData = array([
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

    def __init__(self, renderer):
        super(BoxRenderer, self).__init__(renderer)
        self.camToClipMat = self.renderer.camToClipMat

        self.program = ModelRenderer.compileProgram(
            "shaders/boxvs.glsl", "shaders/boxfs.glsl")

        with self.program:
            self.vertDataBuff = vbo.VBO(self.vertexData)
            self.idxBuff = vbo.VBO(self.indices, 
                target="GL_ELEMENT_ARRAY_BUFFER")

            self.modelToCamMatUnif = glGetUniformLocation(
                self.program, "modelToCamMat")
            self.camToClipMatUnif = glGetUniformLocation(
                self.program, "camToClipMat")
            glUniformMatrix4fv(self.camToClipMatUnif, 1, True, 
                self.camToClipMat)
            
            self.vao = VAO()
            
            with self.vao:
                self.vertDataBuff.bind()
                glEnableVertexAttribArray(0)
                glEnableVertexAttribArray(1)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 
                    self.vertDataBuff)
                glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 
                    self.vertDataBuff + 3*4*4)

                self.idxBuff.bind()

    def draw(self, matrix):
        glUniformMatrix4fv(self.modelToCamMatUnif, 1, True, matrix)
        glDrawElements(GL_TRIANGLES, len(self.indices), 
            GL_UNSIGNED_SHORT, self.idxBuff)

    def drawModels(self, models):
        with self.program:
            with self.vao:
                for m in models:
                    self.draw(m.getModelToWorldMat())
