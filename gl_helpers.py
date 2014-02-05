#!/usr/bin/env python2

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
