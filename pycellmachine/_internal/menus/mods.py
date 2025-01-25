import pygame, os
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
from pycellmachine._internal import mods
import pycellmachine._internal.menus as menus

class ModsMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "mods_title",
            (menu.screen_size()[0]//2, 50),
            (200, 30),
            text="Mods",
            font_color=(255,255,255),
            font_size=80,
            font='Monocraft'
        ), "text")
        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Back', font='Monocraft'
        ), "button")

        mod_paths = [(mod, os.path.getctime(os.path.join(tx.get_resource_path("./mods"), mod))) 
            for mod in os.listdir(tx.get_resource_path("./mods"))]
        sorted_mods = [mod for mod, _ in sorted(mod_paths, key=lambda x: x[1], reverse=True)]

        y = 50
        # sort mods by recently changed
        for mod in sorted_mods:
            y += 110
            self.add_object(menu.Box(
                "text_" + mod,
                (menu.screen_size()[0]//2, y),
                (750, 100),
                texture=tx.asset("ui/box.png"),
                splices=tx.data("ui/box.json"),
                default=True if mod in settings.get()['mods'] else False
            ), "box")
            self.add_object(menu.Image(
                "image_" + mod,
                (menu.screen_size()[0]//2 - 330, y - 5),
                (80, 80),
                texture=mods.path(mod=mod, path='/mod.png')
            ), "image")
            self.add_object(menu.Text(
                "name_" + mod,
                (menu.screen_size()[0]//2, y - 26),
                (550, 100),
                text=mods.load_data(mods.path(mod=mod, path='/mod.json'))['name'],
                font_color=(255,255,255),
                font_size=24,
                font='Monocraft',
                align='left'
            ), "text")
            self.add_object(menu.Text(
                "author_" + mod,
                (menu.screen_size()[0]//2, y - 30),
                (720, 100),
                text=mods.load_data(mods.path(mod=mod, path='/mod.json'))['author'],
                font_color=(255,255,255), font_size=16, font='Monocraft', align='right'
            ), "text")
            self.add_object(menu.Text(
                "description_" + mod,
                (menu.screen_size()[0]//2, y),
                (550, 100),
                text=mods.load_data(mods.path(mod=mod, path='/mod.json'))['description'],
                font_color=(255,255,255),
                font_size=16,
                font='Monocraft',
                align='left'
            ), "text")
    
    def draw(self):
        self.render()
        for text in self.objects['text']:
            text.draw(self.screen)
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    global game_menu
                    game_menu = menus.MainMenu(self.screen)
        for box in self.objects['box']:
            if box.id.startswith('text_'):
                _settings = settings.get()
                if box.value == True and _settings['mods'].count(box.id.split('_')[1]) == 0:
                    _settings['mods'].append(box.id.split('_')[1])
                    settings.save(_settings)
                elif box.value == False and _settings['mods'].count(box.id.split('_')[1]) == 1:
                    _settings['mods'].remove(box.id.split('_')[1])
                    settings.save(_settings)