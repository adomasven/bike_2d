#!/usr/bin/env python2

from basecomponent import Component
from numpy import matrix
from glhelpers import *

MODEL_BOX = 0

class Model(Component):
    def getModelToWorldMat():
        return identityMatrix()


class BoxModel(Model):

    def __init__(self, x=0, y=0, width=10, height=10):
        self.type = MODEL_BOX
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.modelToWorldMat = self.getModelToWorldMat()

    def getModelToWorldMat(self):
        mat = identityMatrix()
        mat[0,0] = self.width / 2
        mat[1,1] = self.height / 2
        mat[0,3] = self.x + self.width / 2
        mat[1,3] = self.y + self.height / 2
        return mat
