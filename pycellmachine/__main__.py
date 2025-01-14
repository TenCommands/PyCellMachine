import pygame
import sys, json
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

def update(self, event):
    for type in self.menu.objects:
        for object in self.menu.objects[type]:
            object.update(event)

class MainMenu():
    def __init__(self):
        self.menu = menu.Screen(screen)
        # Leave Game Button #
        self.menu.add_object(menu.Button(
            "exit_button",
            (300, 300),
            (200, 30),
            texture=tx.asset("button.png"),
            texture_splices=[
                tx.data("button_normal.json"),
                tx.data("button_hover.json")
            ],
            font_size=20, font_color=(255,255,255), text='Leave Game', font='Arial'
        ), "button")

        # Settings Button #
        self.menu.add_object(menu.Button(
            "settings_button",
            (300, 350),
            (200, 60),
            texture=tx.asset("button.png"),
            texture_splices=[
                tx.data("button_normal.json"),
                tx.data("button_hover.json")
            ],
            font_size=20, font_color=(255,255,255), text='Settings', font='Arial'
        ), "button")

    def draw(self):
        self.menu.draw()
    def events(self, event):
        update(self, event)
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

        # Load settings from settings.json
        with open('settings.json') as f:
            settings = json.load(f)['options']

        # Create Text and Box objects for each setting
        y = 200
        for key, value in settings.items():
            section = key
            self.menu.add_object(menu.Text(
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
                self.menu.add_object(menu.Text(
                    key + '_label',
                    (200, y),
                    (200, 30),
                    text=key.replace('_',' ').replace('.',' ').title(),
                    font_color=(255,255,255),
                    font_size=20,
                    font='Monocraft'
                ), "text")
                if isinstance(value, bool):
                    self.menu.add_object(menu.Box(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (30, 30),
                        default=value,
                        texture=tx.asset("box.png"),
                        texture_splices=[
                            tx.data("box_off.json"),
                            tx.data("box_on.json")
                        ]
                    ), "box")
                if isinstance(value, float):
                    self.menu.add_object(menu.Slider(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (300, 30),
                        default=50,
                        values=range(0, 100),
                        texture=tx.asset("slider.png"),
                        texture_splices=[
                            tx.data("slider.json"),
                            tx.data("clear.json"),
                            tx.data("slider_bar.json")
                        ]
                    ), "slider")
                if isinstance(value, str):
                    self.menu.add_object(menu.Keybind(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (300, 30),
                        default=value.replace('_',' ').replace('.',' ').title(),
                        texture=tx.asset("keybind.png"),
                        texture_splices=[
                            tx.data("keybind_normal.json"),
                            tx.data("keybind_hover.json")
                        ],
                        font_color=(255,255,255), font='Monocraft', font_size=20
                    ), "keybind")
                if isinstance(value, list):
                    self.menu.add_object(menu.Dropdown(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (300, 30),
                        default=value[1:].index(value[0]),
                        options=value[1:],
                        texture=tx.asset("dropdown.png"),
                        texture_splices=[
                            tx.data("dropdown_normal.json"),
                            tx.data("dropdown_hover.json")
                        ],
                        font_size=20, font_color=(255,255,255), font='Monocraft'
                    ), "dropdown")
                    
                y += 100
                

        self.menu.add_object(menu.Text(
            "settings_title",
            (screen_size()[0]//2, 50),
            (200, 30),
            text="Settings",
            font_color=(255,255,255),
            font_size=80,
            font='Monocraft'
        ), "text")

        self.menu.add_object(menu.Scrollbar(
            "settings_scrollbar",
            (screen_size()[0]-40, screen_size()[1]//2),
            (20, screen_size()[1]-30),
            texture=tx.asset("slider.png"),
            texture_splices=[
                tx.data("slider.json"),
                tx.data("slider_bar.json")
            ]
        ), "scrollbar")

        self.menu.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("button.png"),
            texture_splices=[
                tx.data("button_normal.json"),
                tx.data("button_hover.json")
            ],
            font_size=20, font_color=(255,255,255), text='Back', font='Monocraft'
        ), "button")

    def draw(self):
        self.menu.draw()
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(str(''), True, (255,255,255))
        screen.blit(text)

    def save_settings(self):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            settings['options'] = {}
        for key, value in self.menu.objects.items():
            if key == "button" or key == "text" or key == "scrollbar":
                continue
            for obj in value:
                section = obj.id.split('.')[0]
                name = obj.id.split('.')[1]
                if section not in settings['options']:
                    settings['options'][section] = {}
                if isinstance(obj, menu.Box):
                    settings['options'][section][name] = obj.value
                if isinstance(obj, menu.Keybind):
                    settings['options'][section][name] = obj.value
                if isinstance(obj, menu.Slider):
                    settings['options'][section][name] = obj.value/100
                if isinstance(obj, menu.Dropdown):
                    # put obj.values[obj.value] at the begging of the obj.values list

                    obj.values.insert(0, obj.values[obj.value])
                    settings['options'][section][name] = obj.values
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)


    def events(self, event):
        update(self, event)
        for scrollbar in self.menu.objects['scrollbar']:
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                scrollbar.update(event)
                scrollbar.scroll(self.menu, scale=-5.1, exclude=['settings_scrollbar', 'settings_title', 'back_button'])
        for button in self.menu.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    self.save_settings()
                    global game_menu
                    game_menu = MainMenu()


game_menu = SettingsMenu()

def main():
    while True:
        screen.fill((100, 100, 100))

        for event in pygame.event.get():
            default_events(event)
            game_menu.events(event)
        
        game_menu.draw()
        
        
        pygame.display.update()

        dt = delta_time(clock, 60)

if __name__ == "__main__":
    game = main()
    game.run()
