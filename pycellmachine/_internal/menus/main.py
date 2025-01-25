import pygame, sys
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
import pycellmachine._internal.menus as menus

class MainMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen

        self.add_object(menu.Image(
            "title",
            (menu.screen_size()[0] // 2, 100),
            (1578, 160),
            texture=tx.get_resource_path('./_internal/assets/title.png')
        ), "image")

        self.add_object(menu.Button(
            "play_button",
            (300, 250),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Play', font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "settings_button",
            (300, 300),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Settings', font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "texturepacks_button",
            (300, 350),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Texture Packs', font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "mods_button",
            (300, 400),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Mods', font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "credits_button",
            (300, 450),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Credits', font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "exit_button",
            (300, 500),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Leave Game', font='Monocraft'
        ), "button")

    def draw(self):
        self.render()
        # draw a transparent black rectangle over the screen that fades out over a second
        if 10 > pygame.time.get_ticks() / 1000 > 5:
            time = int((5000 - pygame.time.get_ticks()) / 1000)
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, menu.screen_size()[0], menu.screen_size()[1]), time)

    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "exit_button":
                    pygame.quit()
                    sys.exit()
                if button.id == "settings_button":
                    game_menu = menus.SettingsMenu(self.screen)
                if button.id == "texturepacks_button":
                    game_menu = menus.TexturepacksMenu(self.screen)
                if button.id == "mods_button":
                    game_menu = menus.ModsMenu(self.screen)
                if button.id == "credits_button":
                    game_menu = menus.CreditsMenu(self.screen)