import pygame, sys
import pygame.scrap
from win32api import GetSystemMetrics
from . import textures as tx

def display_size():
    return (GetSystemMetrics(0), GetSystemMetrics(1))

def window_size():
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    return (w, h)

def screen_size():
    w, h = pygame.display.get_surface().get_size()
    return (w, h)

class Object:
    def is_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def move(self, pos):
        # Move the object to a new position
        self.x = pos[0]
        self.y = pos[1]
        # remake rect object with the new position at the center
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
        # Move any additional rects if they exist
        if hasattr(self, 'chips'):
            for i, chip in enumerate(self.chips):
                chip.x = self.x + (self.width/len(self.values))*i - self.width/2 + (self.width/len(self.values))/2 - 7.5
                chip.y = self.y - self.height/2
    
        if hasattr(self, 'value_rect'):
            if hasattr(self, 'values'):  # For Slider objects
                self.value_rect.x = self.x + (self.width/len(self.values))*self.value - self.width/2 + (self.width/len(self.values))/2 - 7.5
                self.value_rect.y = self.y - self.height/2 - 4
            else:  # For Scrollbar objects
                self.value_rect.x = self.x - self.width/2 - 4
                self.value_rect.y = self.y + self.height/2 - (self.height * self.value) - self.value_rect.height/2



    def size(self, size):
        self.width = size[0]
        self.height = size[1]
        self.move((self.x, self.y))
    
    def draw_splices(self, splices, screen, rect, width, height):
        width = max(width, 1)
        height = max(height, splices['(0, 0)'].get_height() + splices['(0, 2)'].get_height() + 1)

        # Left side
        screen.blit(splices['(0, 0)'], (rect.x, rect.y))
        screen.blit(pygame.transform.scale(splices['(0, 1)'], (splices['(0, 1)'].get_width(), height - splices['(0, 0)'].get_height() - splices['(0, 2)'].get_height())), (rect.x, rect.y + splices['(0, 0)'].get_height()))
        screen.blit(splices['(0, 2)'], (rect.x, rect.y + height - splices['(0, 2)'].get_height()))

        # Calculate dimensions
        middle_width = max(0, width - splices['(0, 0)'].get_width() - splices['(2, 0)'].get_width()) + 1
        middle_height = max(0, height - splices['(0, 0)'].get_height() - splices['(0, 2)'].get_height()) + 1

        # Now the scaling won't use negative values
        middle_top = pygame.transform.scale(splices['(1, 0)'], (middle_width, splices['(1, 0)'].get_height()))
        middle_center = pygame.transform.scale(splices['(1, 1)'], (middle_width, middle_height))
        middle_bottom = pygame.transform.scale(splices['(1, 2)'], (middle_width, splices['(1, 2)'].get_height()))

        screen.blit(middle_top, (rect.x + splices['(0, 0)'].get_width(), rect.y))
        screen.blit(middle_center, (rect.x + splices['(0, 1)'].get_width(), rect.y + splices['(1, 0)'].get_height()))
        screen.blit(middle_bottom, (rect.x + splices['(0, 2)'].get_width(), rect.y + height - middle_bottom.get_height()))

        # Right side
        screen.blit(splices['(2, 0)'], (rect.x + width - splices['(2, 0)'].get_width(), rect.y))
        screen.blit(pygame.transform.scale(splices['(2, 1)'], (splices['(2, 1)'].get_width(), height - splices['(2, 0)'].get_height() - splices['(2, 2)'].get_height())), (rect.x + width - splices['(2, 1)'].get_width(), rect.y + splices['(2, 0)'].get_height()))
        screen.blit(splices['(2, 2)'], (rect.x + width - splices['(2, 2)'].get_width(), rect.y + height - splices['(2, 2)'].get_height()))



class Button(Object):
    def __init__(self, id, pos, size, texture=None, splices=None, font_size=20, font_color=(255,255,255), text='', font='Arial'):
        pygame.font.init()
        self.id = id
        self.text = text
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['normal']),
            tx.splice(self.texture, splices['hover'])
        ]
    
    def draw(self, screen):
        if self.is_hover():
            splices = self.splices[1]
        else:
            splices = self.splices[0]
        
        self.draw_splices(splices, screen, self.rect, self.width, self.height)

        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, event):
        pass

class Slider(Object):
    def __init__(self, id, pos, size, values, default=0, texture=None, splices=None, chips=True):
        self.chips = chips
        self.clicked = False
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.values = values
        self.value = default
        self.width = size[0]
        self.height = size[1]
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['background']),
            tx.splice(self.texture, splices['chip']),
            tx.splice(self.texture, splices['bar'])
        ]

        self.chips = []
        for i in range(len(values)):
            # add rect to self.bar_positions for each value
            self.chips.append(
                pygame.Rect(self.x + (self.width/len(values))*i - self.width/2 + (self.width/len(values))/2 - 7.5,
                            self.y - self.height/2,
                            15,
                            self.height)
            )

        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

        # create rect for the current value
        self.value_rect = pygame.Rect(self.x + (self.width/len(values))*self.value - self.width/2 + (self.width/len(values))/2 - 7.5,
                            self.y - self.height/2 - 4,
                            15,
                            self.height + 6)

    def draw(self, screen):
        splices = self.splices[0]
        self.draw_splices(splices, screen, self.rect, self.width, self.height)
        if self.chips == True:
            splices = self.splices[1]
            # draw bars in self.bars
            for i in range(len(self.chips)):
                self.draw_splices(splices, screen, self.chips[i], self.chips[i].width, self.chips[i].height)
        splices = self.splices[2]
        self.draw_splices(splices, screen, self.value_rect, self.value_rect.width, self.value_rect.height)

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and self.is_hover()) or (event.type == pygame.MOUSEMOTION and self.clicked):
            self.clicked = True

            # set sorted_chips to sort self.chips based on their x distance from the mouse position
            sorted_chips = sorted(self.chips, key=lambda chip: abs(chip.x - pygame.mouse.get_pos()[0]))

            for i in range(len(sorted_chips)):
                if self.chips[i] == sorted_chips[0]:
                    values = self.values
                    self.value = i
                    self.value_rect = pygame.Rect(self.x + (self.width/len(values))*self.value - self.width/2 + (self.width/len(values))/2 - 7.5,
                        self.y - self.height/2 - 4,
                        15,
                        self.height + 6)

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    
    def get_value(self):
        return self.values[self.value]

class Scrollbar(Object):
    def __init__(self, id, pos, size, default=1.0, texture=None, splices=None):
        self.relative_y = 0
        self.previous_y = 0
        self.clicked = False
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.value = default
        self.width = size[0]
        self.height = size[1]
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['background']),
            tx.splice(self.texture, splices['bar'])
        ]

        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.value_rect = pygame.Rect(self.x - self.width/2 - 4, 
                                    self.y + self.height/2 -+ (self.height * self.value),
                                    self.width + 8, 
                                    15)

    def draw(self, screen):
        splices = self.splices[0]
        self.draw_splices(splices, screen, self.rect, self.width, self.height)
        splices = self.splices[1]
        self.draw_splices(splices, screen, self.value_rect, self.value_rect.width, self.value_rect.height)

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and self.is_hover()) or (event.type == pygame.MOUSEMOTION and self.clicked):
            self.clicked = True
            mouse_y = pygame.mouse.get_pos()[1]
            self.relative_y = mouse_y - (self.y - self.height/2)
            #if relative_y < 0:
            #    self.direction = -1
            self.value = 1 - (self.relative_y / self.height)
            self.value = max(0, min(1, self.value))
            
            self.value_rect.y = self.y + self.height/2 - (self.height * self.value) - self.value_rect.height/2

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

    def scroll(self, menu, scale=1, exclude = []):
        if self.clicked:
            scroll_value = self.get_value()
            if 0 < scroll_value < 1:
                move_y = self.relative_y - self.previous_y if hasattr(self, 'previous_y') else 0
                menu.move(0, move_y * scale, exclude=exclude)
                self.previous_y = self.relative_y
    
    def get_value(self):
        return self.value

class Box(Object):
    def __init__(self, id, pos, size, default = False, texture=None, splices=None):
        self.clicked = False
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.value = default
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['on']),
            tx.splice(self.texture, splices['off'])
        ]
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
    def draw(self, screen):
        if self.value:
            splices = self.splices[0]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        else:
            splices = self.splices[1]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
    
    def update(self, event):
        self.clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hover():
            self.value = not self.value
            self.clicked = True

class Keybind(Object):
    def __init__(self, id, pos, size, default=None, texture=None, splices=None, font_size=20, font_color=(255,255,255), font='Arial'):
        self.clicked = False
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.value = default
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['normal']),
            tx.splice(self.texture, splices['hover'])
        ]
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
    def draw(self, screen):
        if not self.is_hover() and not self.clicked:
            splices = self.splices[0]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        else:
            splices = self.splices[1]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        text = self.font.render(str(self.value), True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hover():
            self.clicked = True
        if event.type == pygame.KEYDOWN and self.clicked:
            self.value = pygame.key.name(event.key).capitalize()
            self.clicked = False

class Dropdown(Object):
    def __init__(self, id, pos, size, options=[None, None], default=None, texture=None, splices=None, font_size=20, font_color=(255,255,255), font='Arial'):
        self.clicked = False
        self.hovering = -1
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.value = default
        self.values = options
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['normal']),
            tx.splice(self.texture, splices['hover'])
        ]
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
    
    def draw(self, screen):
        if not self.clicked:
            splices = self.splices[0]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        else:
            splices = self.splices[1]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
            # render all possible values
            splices = self.splices[0]
            
            box_rect = pygame.Rect(self.x - self.width/2, self.y + self.height/2, self.width, self.height * len(self.values))
            self.draw_splices(splices, screen, box_rect, self.width, self.height * len(self.values))

            for i, value in enumerate(self.values):
                text = self.font.render(str(value), True, self.font_color)
                text_rect = text.get_rect(center=(self.rect.center[0], self.rect.center[1] + (i * self.height + self.height)))
                box_rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2 + (i * self.height + self.height),self.width, self.height)
                screen.blit(text, text_rect)
                if box_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hovering = i
        
        if self.values:  # check if values attribute is not empty
            text = self.font.render(str(self.values[self.value]), True, self.font_color)
        else:
            text = self.font.render("", True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked:
            self.clicked = False
            if self.hovering != -1:
                self.value = self.hovering
                self.hovering = -1
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hover():
            self.clicked = True
        
class Textbox(Object):
    def __init__(self, id, pos, size, default='', texture=None, splices=None, allow=None, max_length=None, font_size=20, font_color=(255,255,255), font='Arial'):
        self.clicked = False
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.text = default
        self.texture = pygame.image.load(texture).convert_alpha()
        self.splices = [
            tx.splice(self.texture, splices['normal']),
            tx.splice(self.texture, splices['hover'])
        ]
        self.allowed = allow
        self.max_length = max_length
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    def draw(self, screen):
        if not self.clicked:
            splices = self.splices[0]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        else:
            splices = self.splices[1]
            self.draw_splices(splices, screen, self.rect, self.width, self.height)
        text = self.font.render(str(self.text), True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hover():
            self.clicked = True
            return
        if event.type == pygame.KEYDOWN and self.clicked:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.scrap.put_text(self.text)
                return

            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                clipboard_text = pygame.scrap.get_text()
                if clipboard_text:
                    if self.allowed is None:
                        self.text += clipboard_text
                    else:
                        self.text += ''.join(c for c in clipboard_text if c in self.allowed)
                return

            if event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.scrap.put_text(self.text)
                self.text = ''
                return

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.backspace = True
            elif event.key == pygame.K_RETURN:
                self.clicked = False
            elif self.allowed is None or event.unicode in self.allowed:
                self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = False
        if event:
            if self.max_length is not None and len(self.text) > self.max_length:
                self.text = self.text[:self.max_length]
        
class Text(Object):
    def __init__(self, id, pos, size, text='', font_size=20, font_color=(255,255,255), font='Arial', align='center'):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.align = align

    def draw(self, screen):
        text = self.font.render(str(self.text), True, self.font_color)
        if self.align == 'left':
            text_rect = text.get_rect(midleft=self.rect.midleft)
        elif self.align == 'right':
            text_rect = text.get_rect(midright=self.rect.midright)
        else:  # center alignment
            text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    
    def update(self, event):
        pass

class Image(Object):
    def __init__(self, id, pos, size, texture):
        self.id = id,
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.image = pygame.image.load(texture).convert_alpha()
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    def draw(self, screen):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(scaled_image, self.rect)
        
    def update(self, event):
        pass

class App:
    def __init__(self):
        self.game_menu = None
    
    def change_menu(self, menu):
        self.game_menu = menu

class Screen(App):
    def __init__(self, screen):
        pygame.font.init()
        self.screen = screen
        self.objects = {}
        self.font = pygame.font.SysFont('Arial', 20)

    def add_object(self, object, type):
        if type not in self.objects:
            self.objects[type] = []
        self.objects[type].append(object)

    def render(self):
        for type in self.objects:
            for object in self.objects[type]:
                object.draw(self.screen)
    
    def update(self, event):
        for type in self.objects:
            for object in self.objects[type]:
                object.update(event)
    
    def move(self, offset_x, offset_y, exclude: Object=[]):
        for type in self.objects:
            for object in self.objects[type]:
                if object.id not in exclude:
                    new_x = object.x + offset_x
                    new_y = object.y + offset_y
                    object.move((new_x, new_y))