#!/usr/bin/env python2

from numpy import matrix

class Box():

    def __init__(self, x=0, y=0, width=10, height=10):
        self.type = 'box'
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.modelToWorldMat = self.getModelToWorldMat()

    def draw(self, renderer):
        renderer.draw(self)

    def getModelToWorldMat(self):
        mat = matrix([[0]*4]*4, 'f4')
        # mat[0,0] = self.width
        # mat[1,1] = self.height
        # mat[3,0] = self.x
        # mat[3,1] = self.y
        return mat
