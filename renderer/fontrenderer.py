#!/usr/bin/env python2

from __future__ import division

from modelrenderer import *
from numpy import array
from sdl2 import *
from OpenGL.GL import *
from OpenGL.arrays import vbo #wrapper for vertex buffer objects
from glhelpers import *

class FontRenderer(ModelRenderer):
    vertexData = array([
         #Uses same coordinates for texture and vertices
        -1, -1, 0, 1,
        -1,  1, 0, 0,
         1,  1, 1, 0,
         1, -1, 1, 1
        ], 'f4')

    indices = array([
        0, 1, 2,
        0, 2, 3
        ], 'u2')
    def __init__(self, renderer):
        super(FontRenderer, self).__init__(renderer)

        self.program = ModelRenderer.compileProgram(
            "shaders/fontvs.glsl", "shaders/fontfs.glsl")

        with self.program:
            self.glTexObj = glGenTextures(1)

            self.vertDataBuff = vbo.VBO(self.vertexData)
            self.idxBuff = vbo.VBO(self.indices, 
                target="GL_ELEMENT_ARRAY_BUFFER")

            self.transformMatUnif = glGetUniformLocation(
                self.program, "transformMat")
            self.glTexUnif = glGetUniformLocation(self.program, 'tex')
            
            self.vao = VAO()
            
            with self.vao:
                self.vertDataBuff.bind()
                glEnableVertexAttribArray(0)
                glEnableVertexAttribArray(1)
                glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, 
                    self.vertDataBuff)
                glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, 
                    self.vertDataBuff + 4*2)

                self.idxBuff.bind()
        

    def draw(self, surface, model):
        with self.program:
            with self.vao:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.glTexObj)
                glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
                glTexImage2D(GL_TEXTURE_2D, 0, 
                    GL_RGBA, 
                    surface.w, surface.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, 
                    GLvoidp(surface.pixels))
                glUniform1i(self.glTexUnif, 0)

                mat = model.getModelToWorldMat()
                mat[0, 0] /= self.renderer.winWidth
                mat[1, 1] /= self.renderer.winHeight
                mat[0, 3] = (mat[0, 3] - self.renderer.winWidth) / \
                    self.renderer.winWidth
                mat[1, 3] = (mat[1, 3] - self.renderer.winHeight) / \
                    self.renderer.winHeight
                glUniformMatrix4fv(self.transformMatUnif, 1, True, mat)
                glDrawElements(GL_TRIANGLES, len(self.indices), 
                    GL_UNSIGNED_SHORT, self.idxBuff)
