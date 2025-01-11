import pygame, sys
from win32api import GetSystemMetrics

def display_size():
    return (GetSystemMetrics(0), GetSystemMetrics(1))

def window_size():
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    return (w, h)

class Button:
    def __init__(self, id, pos, size, texture=None, color=[(100,100,100),(50,50,50)], text_size=20, font_color=(255,255,255), text='', font='Arial'):
        pygame.font.init()
        self.id = id
        self.text = text
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        if texture == None:
            self.color = color[0]
            self.hover_color = color[1]
        self.font = pygame.font.SysFont(font, text_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def move(self, pos):
        # Move the button to a new position
        self.x = pos[0]
        self.y = pos[1]
        # remake rect object with the new position at the center
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    
    def size(self, size):
        self.width = size[0]
        self.height = size[1]
        self.move((self.x, self.y))
    
    def update(self):
        self.size((self.width, self.height))

class Slider:
    def _init__(self, id, start, end, step, width, height, color, hover_color, font_color):
        self.id = id
        self.start = start
        self.end = end
        self.step = step
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 20)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Screen:
    def __init__(self, screen):
        pygame.font.init()
        self.screen = screen
        self.objects = {}
        self.font = pygame.font.SysFont('Arial', 20)

    def add_object(self, object, type):
        if type not in self.objects:
            self.objects[type] = []
        self.objects[type].append(object)

    def draw(self):
        for type in self.objects:
            for object in self.objects[type]:
                object.update()
                object.draw(self.screen)