#!/usr/bin/env python2

from math import cos, sin

from OpenGL.GL import *
from numpy import array

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
    mat = array([[0]*4]*4, 'f4')
    for i in range(4):
        mat[i,i] = 1

    return mat

def rotationMatrix(angle):
    rot = identityMatrix()
    rot[0,0] = cos(angle)
    rot[0,1] = -sin(angle)
    rot[1,0] = sin(angle)
    rot[1,1] = cos(angle)

    return rot