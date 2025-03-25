import pygame, json, numpy as math, base64
from pycellmachine._internal import settings
from pycellmachine._internal import textures as tx
from pycellmachine._internal import mods

#pygame.init()

x, y = 0, 0

class vec(tuple):
    """A N-Dimensional vector"""
    def __new__(cls, *args):
        return tuple.__new__(cls, args)
    def __add__(self, other):
        return vec(*[self[i] + other[i] for i in range(len(self))])
    def __sub__(self, other):
        return vec(*[self[i] - other[i] for i in range(len(self))])
    def __mul__(self, other):
        return vec(*[self[i] * other[i] for i in range(len(self))])
    def __truediv__(self, other):
        return vec(*[self[i] / other[i] for i in range(len(self))])
    def __floordiv__(self, other):
        return vec(*[self[i] // other[i] for i in range(len(self))])
    def __mod__(self, other):
        return vec(*[self[i] % other[i] for i in range(len(self))])
    def __pow__(self, other):
        return vec(*[self[i] ** other[i] for i in range(len(self))])
class vec2(vec):
    """A 2D vector"""
    def __new__(cls, x, y):
        return vec.__new__(cls, (x, y))

def vec2_to_deg(vec: vec2) -> float:
    """Converts a 2D vector (x, y) to degrees."""
    angle_rad = math.arctan2(vec[1], vec[0])
    angle_deg = math.degrees(angle_rad) % 360
    return angle_deg

def deg_to_vec2(deg: float) -> vec2:
    """Converts degrees to a 2D vector (x, y)."""
    rad = math.radians(deg)
    x = math.cos(rad)
    y = math.sin(rad)
    return vec2(x, y)

def shrink_text(text: str) -> str:
    """Shrinks long text into a short string without losing data."""
    ascii = ""
    # convert text into ascii
    for char in text:
        ascii += str(ord(char))
    # convert ascii to integer
    ascii = int(ascii)
    i = 0 # keep track of how many times we divided by 2
    while ascii % 2 == 0:
        ascii = ascii // 2
        i += 1
    # first digit is the length of the number idicating how many times we divided by 2
    # second digit is the number of times we divided by 2
    # third digit is the ascii value which was repeatedly divided by 2
    return f"{len(str(i))}{i}{ascii}"

def register_cell(name: str):
    def decorator(cls):
        mods.register_cell(name, cls)
        return cls
    return decorator

class Grid:
    def __init__(self, width: int, height: int, scale: int=1, offset: vec2=vec2(0, 0)):
        self.width = width
        self.height = height
        self.scale = scale
        self.x = 0
        self.y = 0
        self.grid = [[None for _ in range(width)] for _ in range(height)] # 2D array of Cell objects

    def _move(self, x: int, y: int):
        self.x += x
        self.y += y
    
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = settings.get('options')['keybinds']
            if event.key == getattr(pygame, 'K_' + keys['up']):
                self.move(0, -1)
            if event.key == getattr(pygame, 'K_' + keys['left']):
                self.move(-1, 0)
            if event.key == getattr(pygame, 'K_' + keys['down']):
                self.move(0, 1)
            if event.key == getattr(pygame, 'K_' + keys['right']):
                self.move(1, 0)
    
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    # check if self.grid[y][x] has a draw method
                    if hasattr(self.grid[y][x], 'draw'):
                        self.grid[y][x].draw(screen)
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), (x * self.scale, y * self.scale, self.scale, self.scale))
    
    def tick(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    self.grid[y][x].tick()
    
    def add_cell(self, cell):
        self.grid[cell.y][cell.x] = cell
    
    def remove_cell(self, cell):
        self.grid[cell.y][cell.x] = None
    
    def get_cell(self, x: int, y: int):
        return self.grid[y][x]
    
    def _level_code(self):
        data = f"{len(self.width)}{self.width}{len(self.height)}{self.height}"
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    data += self.grid[y][x].mod_namespace + "." + self.grid[y][x].name
        return data
    
    def _load_level(self, data: str):
        width_len = int(data[0])
        width = ""
        for i in range(1, width_len + 1):
            width += data[i]

class Cell:
    def __init__(self, id, pos, dir, flags=[], priority=0):
        self.id = id
        self.pos = pos
        self.dir = dir
        self.flags = flags
        self.priority = priority