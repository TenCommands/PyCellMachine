import pygame, sys, os, json
from ._internal import settings
from ._internal import textures as tx
from ._internal import mods

pygame.init()

class Cell(pygame.sprite.Sprite):
    def __init__(self,
                 cell_id: str,
                 pos: tuple,
                 dir: tuple,
                 flags: list = [],
                 priority: int = 0
        ):
        pygame.sprite.Sprite.__init__(self)
        self.cell_id = cell_id
        self.x = pos[0]
        self.y = pos[1]
        self.dir = dir
        self.flags = flags
        self.priority = priority
    
    def neighbors(self, relative_pos=[(1,0),(-1,0),(0,1),(0,-1)]):
        neighbors = []
        for x, y in relative_pos:
            neighbors.append((self.x + x, self.y + y))
        return neighbors

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, cell_id):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.cell_id = cell_id
