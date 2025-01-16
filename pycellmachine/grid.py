import pygame, sys, os, json
from ._internal import settings
from ._internal import textures as tx
from ._internal import mods

pygame.init()

class Grid():
    def __init__(self, size, cell_size):
        self.size = size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.cells = pygame.sprite.Group()
        self.cell_id = 0
        self.cell_size = cell_size
        self.cell_size_x = cell_size[0]
        self.cell_size_y = cell_size[1]
        self.cell_size_x_half = cell_size[0] / 2
        self.cell_size_y_half = cell_size[1] / 2
        self.cell_size_x_half_half = cell_size[0] / 4
        self.cell_size_y_half_half = cell_size[1] / 4
        self.cell_size_x_half_half_half = cell_size[0] / 8
        self.cell_size_y_half_half_half = cell_size

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, cell_id):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.cell_id = cell_id
