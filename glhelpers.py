#!/usr/bin/env python2

from OpenGL.GL import *
from numpy import matrix

'''Usage:

vao = VAO()

with VAO:
    glDrawArrays()

'''
class VAO():
    def __init__(self):
        self.vao = glGenVertexArrays(1)

    def __enter__(self):
        self.bind()

    def __exit__(self, type, val, traceback):
        self.unbind()

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

def identityMatrix():
    mat = matrix([[0]*4]*4, 'f4')
    for i in range(4):
        mat[i,i] = 1

    return mat