import pygame, sys
from win32api import GetSystemMetrics
import src.textures as tx

def display_size():
    return (GetSystemMetrics(0), GetSystemMetrics(1))

def window_size():
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    return (w, h)

class Object:
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


class Button(Object):
    def __init__(self, id, pos, size, texture=None, texture_splices=None, color=[(100,100,100),(50,50,50)], text_size=20, font_color=(255,255,255), text='', font='Arial'):
        pygame.font.init()
        self.id = id
        self.text = text
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.font = pygame.font.SysFont(font, text_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        if texture == None:
            self.color = color[0]
            self.hover_color = color[1]
            self.texture = None
            self.texture_splices = None
        else:
            self.texture = pygame.image.load(texture).convert()
            self.texture_splices = [
                tx.splice(self.texture, texture_splices[0]),
                tx.splice(self.texture, texture_splices[1])
            ]
    
    def draw(self, screen):
        if self.texture == None:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, self.hover_color, self.rect)
            else:
                pygame.draw.rect(screen, self.color, self.rect)
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                splices = self.texture_splices[1]
            else:
                splices = self.texture_splices[0]

            # Left side
            screen.blit(splices['(0, 0)'], (self.rect.x, self.rect.y))
            screen.blit(splices['(0, 1)'], (self.rect.x, self.rect.y + self.height/2 - splices['(0, 1)'].get_height()/2 + 1))
            screen.blit(splices['(0, 2)'], (self.rect.x, self.rect.y + self.height - splices['(0, 2)'].get_height()))
            # Middle (stretched)
            middle_width = self.width - splices['(0, 0)'].get_width() - splices['(2, 0)'].get_width() + 1
            middle_top = pygame.transform.scale(splices['(1, 0)'], (middle_width, splices['(1, 0)'].get_height()))
            middle_center = pygame.transform.scale(splices['(1, 1)'], (middle_width, splices['(1, 1)'].get_height() + 1))
            middle_bottom = pygame.transform.scale(splices['(1, 2)'], (middle_width, splices['(1, 2)'].get_height()))
            screen.blit(middle_top, (self.rect.x + splices['(0, 0)'].get_width(), self.rect.y))
            screen.blit(middle_center, (self.rect.x + splices['(0, 1)'].get_width(), self.rect.y + self.height/2 - middle_center.get_height()/2))
            screen.blit(middle_bottom, (self.rect.x + splices['(0, 2)'].get_width(), self.rect.y + self.height - middle_bottom.get_height()))
            # Right side
            screen.blit(splices['(2, 0)'], (self.rect.x + self.width - splices['(2, 0)'].get_width(), self.rect.y))
            screen.blit(splices['(2, 1)'], (self.rect.x + self.width - splices['(2, 1)'].get_width(), self.rect.y + self.height/2 - splices['(2, 1)'].get_height()/2 + 1))
            screen.blit(splices['(2, 2)'], (self.rect.x + self.width - splices['(2, 2)'].get_width(), self.rect.y + self.height - splices['(2, 2)'].get_height()))

        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Slider(Object):
    def __init__(self, id, pos, size, values, default=0, color=[(100,100,100),(50,50,50),(255,255,255)], texture=None, texture_splices=None):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.values = values,
        self.value = default
        self.width = size[0]
        self.height = size[1]
        if texture == None:
            self.color = color[0]
            self.hover_color = color[1]
            self.bar_color = color[2]
            self.texture = None
            self.texture_splices = None
        else:
            self.texture = pygame.image.load(texture).convert()
            self.texture_splices = [
                tx.splice(self.texture, texture_splices[0]),
                tx.splice(self.texture, texture_splices[1]),
                tx.splice(self.texture, texture_splices[2])
            ]

        self.bar_positions = []
        for x in range(self.x, self.x + self.width):
            self.bar_positions.append((x, self.y))

        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        # draw bar at value position
        pygame.draw.rect(screen, self.bar_color, (self.bar_positions[self.value], (1, self.height)))

        




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