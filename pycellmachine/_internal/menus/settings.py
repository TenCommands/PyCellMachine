import pygame, os
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
import pycellmachine._internal.menus as menus

class SettingsMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        _settings = settings.get('options')

        # Create Text and Box objects for each setting
        y = 200
        for key, value in _settings.items():
            section = key
            self.add_object(menu.Text(
                key,
                (200, y),
                (200, 30),
                text=key.capitalize(),
                font_color=(255,255,255),
                font_size=30,
                font='Monocraft'
            ), "text")
            y += 100
            for key, value in value.items():
                self.add_object(menu.Text(
                    key + '_label',
                    (200, y),
                    (200, 30),
                    text=key.replace('_',' ').replace('.',' ').title(),
                    font_color=(255,255,255),
                    font_size=20,
                    font='Monocraft'
                ), "text")
                if isinstance(value, bool):
                    self.add_object(menu.Box(
                        section + '.' + key,
                        (menu.screen_size()[0]-260, y),
                        (30, 30),
                        default=value,
                        texture=tx.asset("ui/box.png"),
                        splices=tx.data("ui/box.json")
                    ), "box")
                if isinstance(value, float):
                    self.add_object(menu.Slider(
                        section + '.' + key,
                        (menu.screen_size()[0]-260, y),
                        (300, 30),
                        default=50,
                        values=range(0, 100),
                        texture=tx.asset("ui/slider.png"),
                        splices=tx.data("ui/slider.json"),
                        chips=False
                    ), "slide")
                if isinstance(value, str):
                    self.add_object(menu.Keybind(
                        section + '.' + key,
                        (menu.screen_size()[0]-260, y),
                        (300, 30),
                        default=value.replace('_',' ').replace('.',' ').title(),
                        texture=tx.asset("ui/keybind.png"),
                        splices=tx.data("ui/keybind.json"),
                        font_color=(255,255,255), font='Monocraft', font_size=20
                    ), "keybind")
                if isinstance(value, list):
                    self.add_object(menu.Dropdown(
                        section + '.' + key,
                        (menu.screen_size()[0]-260, y),
                        (300, 30),
                        default=value[1:].index(value[0]) if value[0] in value[1:] else 0,
                        options=value[1:],
                        texture=tx.asset("ui/dropdown.png"),
                        splices=tx.data("ui/dropdown.json"),
                        font_size=20, font_color=(255,255,255), font='Monocraft'
                    ), "dropdown")
                    
                y += 100
                

        self.add_object(menu.Text(
            "settings_title",
            (menu.screen_size()[0]//2, 50),
            (200, 30),
            text="Settings",
            font_color=(255,255,255),
            font_size=80,
            font='Monocraft'
        ), "text")

        self.add_object(menu.Scrollbar(
            "settings_scrollbar",
            (menu.screen_size()[0]-40, menu.screen_size()[1]//2),
            (20, menu.screen_size()[1]-30),
            texture=tx.asset("ui/slider.png"),
            splices=tx.data("ui/slider.json")
        ), "scrollbar")

        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Back', font='Monocraft'
        ), "button")

    def draw(self):
        self.render()

    def save_settings(self):
        _settings = settings.get()
        _settings['options'] = {}
        for key, value in self.objects.items():
            if key == "button" or key == "text" or key == "scrollbar":
                continue
            for obj in value:
                section = obj.id.split('.')[0]
                name = obj.id.split('.')[1]
                if section not in _settings['options']:
                    _settings['options'][section] = {}
                if isinstance(obj, menu.Box):
                    _settings['options'][section][name] = obj.value
                if isinstance(obj, menu.Keybind):
                    _settings['options'][section][name] = obj.value
                if isinstance(obj, menu.Slider):
                    _settings['options'][section][name] = obj.value/100
                if isinstance(obj, menu.Dropdown):
                    if 0 <= obj.value < len(obj.values):
                        obj.values.insert(0, obj.values[obj.value])
                    _settings['options'][section][name] = obj.values
        settings.save(_settings)

    def events(self, event, deltaTime):
        self.update(event)
        for scrollbar in self.objects['scrollbar']:
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                scrollbar.update(event)
                scrollbar.scroll(self, scale=-5.1, exclude=['settings_scrollbar', 'settings_title', 'back_button'])
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    self.save_settings()
                    global game_menu
                    game_menu = menus.MainMenu(self.screen)