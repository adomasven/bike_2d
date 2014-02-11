#!/usr/bin/env python2

from OpenGL.GL import shaders #convenience lib for working with shaders
from OpenGL.GL import *

class ModelRenderer(object):
    def __init__(self, renderer):
        self.renderer = renderer

    def drawModels(self, models):
        for m in models:
            self.draw(m)

    @staticmethod
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

