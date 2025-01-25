

import pygame
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
import pycellmachine._internal.menus as menus

class CreditsMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "credits_title",
            (menu.screen_size()[0]//2, 50),
            (200, 30),
            text="Credits",
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
        y = 110
        for line in open(tx.get_resource_path(rf"./credits.txt"), 'r').readlines():
            y += 50
            self.add_object(menu.Text(
                "credits_text",
                (menu.screen_size()[0]//2, y),
                (200, 30),
                text=line,
                font_color=(255,255,255),
                font_size=40,
                font='Monocraft'
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