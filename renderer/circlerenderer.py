#!/usr/bin/env python2

from __future__ import division
from math import pi, tan, cos
from modelrenderer import *
from numpy import array
from sdl2 import *
from OpenGL.GL import *
from OpenGL.arrays import vbo #wrapper for vertex buffer objects
from glhelpers import *

class CircleRenderer(ModelRenderer):
    def __init__(self, renderer, numVerts = 32):
        super(CircleRenderer, self).__init__(renderer)
        self.camToClipMat = self.renderer.camToClipMat
        self.numVerts = numVerts
        self.vertexData = self.generateCirclePoints(numVerts)

        self.program = ModelRenderer.compileProgram(
            "shaders/circlevs.glsl", "shaders/circlefs.glsl")

        with self.program:
            self.vertDataBuff = vbo.VBO(self.vertexData)

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
                glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 
                    self.vertDataBuff)


    def draw(self, matrix):
        glUniformMatrix4fv(self.modelToCamMatUnif, 1, True, matrix)
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(self.vertexData) // 2)

    def drawModels(self, models):
        with self.program:
            with self.vao:
                for m in models:
                    self.draw(m.getModelToWorldMat())

    # this algo stolen from: http://slabode.exofire.net/circle_draw.shtml
    def generateCirclePoints(self, numVerts, skip=4):
        vertexData = [0,  0]

        theta = 2 * pi / numVerts
        tangetial_factor = tan(theta)
        radial_factor = cos(theta)

        x = 1
        y = 0

        for i in range(numVerts -1):
            vertexData.extend([x, y])

            tx = y
            ty = -x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor

        return array(vertexData, dtype='f4')