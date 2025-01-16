import pygame

pygame.init()

class Cell(pygame.sprite.Sprite):
    def __init__(self, pos, cell_id):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.cell_id = cell_id