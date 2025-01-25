import pygame, os
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
import pycellmachine._internal.menus as menus

class TexturepacksMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "texturepacks_title",
            (menu.screen_size()[0]//2, 50),
            (200, 30),
            text="Texturepacks",
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

        # for texturepack in os.listdir(rf"./texturepacks"):
        y = 50
        for texturepack in os.listdir(tx.get_resource_path(rf"./texturepacks")):
            y += 110
            self.add_object(menu.Box(
                "text_" + texturepack,
                (menu.screen_size()[0]//2, y),
                (750, 100),
                texture=tx.asset("ui/box.png"),
                splices=tx.data("ui/box.json")
            ), "box")
            self.add_object(menu.Image(
                "image_" + texturepack,
                (menu.screen_size()[0]//2 - 330, y - 5),
                (80, 80),
                texture=tx.texturepack(pack=texturepack, path='/pack.png')
            ), "image")
            self.add_object(menu.Text(
                "name_" + texturepack,
                (menu.screen_size()[0]//2, y - 26),
                (550, 100),
                text=tx.load_data(tx.texturepack(pack=texturepack, path='/pack.json'))['name'],
                font_color=(255,255,255),
                font_size=24,
                font='Monocraft',
                align='left'
            ), "text")
            self.add_object(menu.Text(
                "author_" + texturepack,
                (menu.screen_size()[0]//2, y - 30),
                (720, 100),
                text=tx.load_data(tx.texturepack(pack=texturepack, path='/pack.json'))['author'],
                font_color=(255,255,255),
                font_size=16,
                font='Monocraft',
                align='right'
            ), "text")
            self.add_object(menu.Text(
                "description_" + texturepack,
                (menu.screen_size()[0]//2, y),
                (550, 100),
                text=tx.load_data(tx.texturepack(pack=texturepack, path='/pack.json'))['description'],
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
                box.value = False
                if box.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                    _settings = settings.get()
                    _settings['texturepack'] = box.id.split('_')[1]
                    settings.save(_settings)