import pygame
import sys
from ._internal import menu
from ._internal import textures as tx

screen = pygame.display.set_mode(menu.display_size(), pygame.RESIZABLE)

clock = pygame.time.Clock()

def delta_time(clock_obj, frame_rate):
    return clock_obj.tick(frame_rate) / 1000.0

def screen_size():
    w, h = pygame.display.get_surface().get_size()
    return (w, h)

def default_events(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()

class MainMenu():
    def __init__(self):
        self.menu = menu.Screen(screen)
        # Leave Game Button #
        self.menu.add_object(menu.Button(
            "exit_button",
            (300, 300),
            (200, 30),
            texture=r"texturepacks\default\assets\button.png",
            texture_splices=[
                r"texturepacks\default\data\button_normal.json",
                r"texturepacks\default\data\button_hover.json"
            ],
            text_size=20, font_color=(255,255,255), text='Leave Game', font='Arial'
        ), "button")

        # Settings Button #
        self.menu.add_object(menu.Button(
            "settings_button",
            (300, 350),
            (200, 30),
            texture=r"texturepacks\default\assets\button.png",
            texture_splices=[
                r"texturepacks\default\data\button_normal.json",
                r"texturepacks\default\data\button_hover.json"
            ],
            text_size=20, font_color=(255,255,255), text='Settings', font='Arial'
        ), "button")

    def draw(self):
        self.menu.draw()
    def events(self, event):
        for button in self.menu.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "exit_button":
                    pygame.quit()
                    sys.exit()
                if button.id == "settings_button":
                    global game_menu
                    game_menu = SettingsMenu()

class SettingsMenu():
    def __init__(self):
        self.menu = menu.Screen(screen)
        self.menu.add_object(menu.Button(
            "back_button",
            (300, 300),
            (200, 30),
            texture=r"texturepacks\default\assets\button.png",
            texture_splices=[
                r"texturepacks\default\data\button_normal.json",
                r"texturepacks\default\data\button_hover.json"
            ],
            text_size=20, font_color=(255,255,255), text='Back', font='Arial'
        ), "button")
        self.menu.add_object(menu.Slider(
            "test_slider",
            (300, 200),
            (200, 30),
            texture=r"texturepacks\default\assets\slider.png",
            texture_splices=[
                r"texturepacks\default\data\slider.json",
                r"texturepacks\default\data\slider_chip.json",
                r"texturepacks\default\data\slider_bar.json"
            ],
            values=range(5),
            default=3,
        ), "slider")
    def draw(self):
        self.menu.draw()
    def events(self, event):
        for button in self.menu.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    global game_menu
                    game_menu = MainMenu()

game_menu = MainMenu()

def main():
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            default_events(event)
            game_menu.events(event)
        
        game_menu.draw()
        pygame.display.update()

        dt = delta_time(clock, 60)

if __name__ == "__main__":
    game = main()
    game.run()
