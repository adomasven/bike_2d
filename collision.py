#!/usr/bin/env python2

from components import *
from vec2d import Vec2d

__all__ = ['CollisionResolver']

def collides(this, other):
    try: bound = this['hitbox'].getBoundingBox(this)
    except:
        try: bound = this['hitbox'].getBoundingCircle(this)
        except: return False

    if bound.intersects(other): return True

    return False


class CollisionResolver(object):
    @staticmethod
    def resolveCollisions(entities):
        for i, this in enumerate(entities):
            for other in entities[i:]:
                if(collides(this, other)):
                    resolveCollision(this, other)

    @staticmethod
    def resolveCollision(this, other):
        try: this['contact'].append(Contact(other))
        except: this['contact'] = Contact(other)

        try: other['contact'].append(Contact(this))
        except: other['contact'] = Contact(this)

class Bounds(object):
    def intersects(self, other):
        ohb = other['hitbox']
        try: return self.intersectsBB(ohb.getBoundingBox(other))
        except:
            try: return self.intersectsCirc(ohb.getBoundingCircle(other))
            except: return False

class BoundingBox(Bounds):
    def __init__(self, x, y, w, h):
        self.pos = Vec2d(x, y)
        self.dim = Vec2d(w, h)

    def intersectsBB(self, other):
        if self.pos.x > other.pos.x + other.dim.w or \
           self.pos.y > other.pos.y + other.dim.h or \
           other.pos.x > self.pos.x + self.dim.w or \
           other.pos.y > self.pos.y + self.dim.h:
            return False
        return True

    def intersectsCirc(self, other):
        return False

class BoundingCircle(Bounds):
    def __init__(self, x, y, r):
        self.pos = Vec2d(x, y)
        self.r = r

    def intersectsCirc(self, other):
        if (self.pos - other.pos).get_length