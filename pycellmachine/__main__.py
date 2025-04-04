import pygame
#pygame.init()
import sys, os, json, traceback
from pycellmachine._internal import get_resource_path
from pycellmachine._internal import logging
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
from pycellmachine._internal import lang
from pycellmachine._internal import mods

#log_file = logging.#log_file("game.log")

#log_file.clear()
#log_file.write("PyCellMachine v0.0.1")

#appicon = pygame.image.load(r'./_internal/assets/logo.png')
pygame.display.set_caption('PyCellMachine')
#pygame.display.set_icon(appicon)

global game_menu
game_menu = None

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

class LoadingMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.loading_image = pygame.image.load(get_resource_path(r'.\_internal\assets\title.png'))
    
    def draw(self):
        if pygame.time.get_ticks() / 1000 > 5:
            # fade out self.loading_image by alpha
            self.loading_image.set_alpha(255 - (pygame.time.get_ticks() / 1000 - 5) * 255)
            if pygame.time.get_ticks() / 1000 > 6:
                global game_menu
                game_menu = MainMenu(screen)
        else: 
            self.loading_image.set_alpha(pygame.time.get_ticks() / 1500 * 255)
        screen.fill((0, 0, 0))
        screen.blit(self.loading_image, (screen_size()[0]//2 - self.loading_image.get_width()//2, screen_size()[1]//2 - self.loading_image.get_height()//2))
    
    def events(self, event, deltaTime):
        self.update(event)

class MainMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Image(
            "title",
            (screen_size()[0] // 2, 100),
            (1578, 160),
            texture=tx.get_resource_path('./_internal/assets/title.png')
        ), "image")

        self.add_object(menu.Button(
            "play_button",
            (300, 250),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.play'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "settings_button",
            (300, 300),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.settings'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "texturepacks_button",
            (300, 350),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.texture_packs'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "mods_button",
            (300, 400),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.mods'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "credits_button",
            (300, 450),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.credits'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "exit_button",
            (300, 500),
            (200, 30),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('main.quit'), font='Monocraft'
        ), "button")

    def draw(self):
        self.render()
        # draw a transparent black rectangle over the screen that fades out over a second
        if 10 > pygame.time.get_ticks() / 1000 > 5:
            time = int((5000 - pygame.time.get_ticks()) / 1000)
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_size()[0], screen_size()[1]), time)

    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "exit_button":
                    pygame.quit()
                    sys.exit()
                if button.id == "play_button":
                    game_menu = PlayMenu(screen)
                if button.id == "settings_button":
                    game_menu = SettingsMenu(screen)
                if button.id == "texturepacks_button":
                    game_menu = TexturepacksMenu(screen)
                if button.id == "mods_button":
                    game_menu = ModsMenu(screen)
                if button.id == "credits_button":
                    game_menu = CreditsMenu(screen)

class PlayMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('back'), font='Monocraft'
        ), "button")
        self.add_object(menu.Button(
            "built_in_button",
            (menu.screen_size()[0] // 2 - 200, 250),
            (60, 60),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='', font='Monocraft'
        ), "button")
        self.add_object(menu.Image(
            "built_in_icon",
            (menu.screen_size()[0] // 2 - 200, 250),
            (50, 50),
            texture=tx.get_resource_path(r".\_internal\assets\built_in.png"),
        ), "image")
        self.add_object(menu.Button(
            "import_level_button",
            (menu.screen_size()[0] // 2, 250),
            (60, 60),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='', font='Monocraft'
        ), "button")
        self.add_object(menu.Image(
            "import_level_icon",
            (menu.screen_size()[0] // 2, 250),
            (50, 50),
            texture=tx.get_resource_path(r".\_internal\assets\import.png"),
        ), "image")
        self.add_object(menu.Button(
            "create_level_button",
            (menu.screen_size()[0] // 2 + 200, 250),
            (60, 60),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='', font='Monocraft'
        ), "button")
        self.add_object(menu.Image(
            "create_level_icon",
            (menu.screen_size()[0] // 2 + 200, 250),
            (50, 50),
            texture=tx.get_resource_path(r".\_internal\assets\create.png"),
        ), "image")
    def draw(self):
        self.render()
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "back_button":
                    game_menu = MainMenu(screen)
                if button.id == "built_in_button":
                    game_menu = BuiltInLevelMenu(screen)
                if button.id == "import_level_button":
                    game_menu = LoadLevelMenu(screen)
                if button.id == "create_level_button":
                    game_menu = CreateLevelMenu(screen)

class BuiltInLevelMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('back'), font='Monocraft'
        ), "button")
    
    def draw(self):
        self.render()
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "back_button":
                    game_menu = PlayMenu(screen)

class LoadLevelMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('back'), font='Monocraft'
        ), "button")
        self.add_object(menu.Textbox(
            "code_textbox",
            (menu.screen_size()[0] // 2, 250),
            (200, 50),
            texture=tx.asset("ui/keybind.png"),
            splices=tx.data("ui/keybind.json"),
            font_size=20, font_color=(255,255,255), font='Monocraft'
        ), "textbox")
        self.add_object(menu.Button(
            "load_button",
            (menu.screen_size()[0] // 2, 250),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('play.load.load'), font='Monocraft'
        ), "button")
    
    def draw(self):
        self.render()
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "back_button":
                    game_menu = PlayMenu(screen)

class CreateLevelMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('back'), font='Monocraft'
        ), "button")
        self.add_object(menu.Textbox(
            "width_textbox",
            (menu.screen_size()[0] // 2 - 120, 400),
            (200, 50),
            texture=tx.asset("ui/keybind.png"),
            splices=tx.data("ui/keybind.json"),
            allow=['0','1','2','3','4','5','6','7','8','9'],
            max_length=5,
            font_size=20, font_color=(255,255,255), font='Monocraft'
        ), "textbox")
        self.add_object(menu.Text(
            "width_text",
            (menu.screen_size()[0] // 2 - 120, 340),
            (200, 50),
            font_size=20, font_color=(255,255,255), font='Monocraft', text=lang.load_lang('play.create.width')
        ), "text")
        self.add_object(menu.Textbox(
            "height_textbox",
            (menu.screen_size()[0] // 2 + 120, 400),
            (200, 50),
            texture=tx.asset("ui/keybind.png"),
            splices=tx.data("ui/keybind.json"),
            allow=['0','1','2','3','4','5','6','7','8','9'],
            max_length=5,
            font_size=20, font_color=(255,255,255), font='Monocraft'
        ), "textbox")
        self.add_object(menu.Text(
            "height_text",
            (menu.screen_size()[0] // 2 + 120, 340),
            (200, 50),
            font_size=20, font_color=(255,255,255), font='Monocraft', text=lang.load_lang('play.create.height')
        ), "text")
        self.add_object(menu.Button(
            "create_button",
            (menu.screen_size()[0] // 2, 500),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text='Create', font='Monocraft'
        ), "button")
    
    def draw(self):
        self.render()
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                global game_menu
                if button.id == "back_button":
                    game_menu = PlayMenu(screen)

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
                        (screen_size()[0]-260, y),
                        (30, 30),
                        default=value,
                        texture=tx.asset("ui/box.png"),
                        splices=tx.data("ui/box.json")
                    ), "box")
                if isinstance(value, float):
                    self.add_object(menu.Slider(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (300, 30),
                        default=50,
                        values=range(0, 101),
                        texture=tx.asset("ui/slider.png"),
                        splices=tx.data("ui/slider.json"),
                        chips=False
                    ), "slider")
                    self.add_object(menu.Text(
                        section + '.' + key + '_value',
                        (screen_size()[0]-480, y),
                        (300, 30),
                        text=str(value*100)+'%',
                        font_color=(255,255,255),
                        font_size=20,
                        font='Monocraft'
                    ), "slider_text")
                if isinstance(value, str):
                    self.add_object(menu.Keybind(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
                        (300, 30),
                        default=value.replace('_',' ').replace('.',' ').title(),
                        texture=tx.asset("ui/keybind.png"),
                        splices=tx.data("ui/keybind.json"),
                        font_color=(255,255,255), font='Monocraft', font_size=20
                    ), "keybind")
                if isinstance(value, list):
                    self.add_object(menu.Dropdown(
                        section + '.' + key,
                        (screen_size()[0]-260, y),
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
            (screen_size()[0]//2, 50),
            (200, 30),
            text=lang.load_lang('settings.title'),
            font_color=(255,255,255),
            font_size=80,
            font='Monocraft'
        ), "text")

        self.add_object(menu.Scrollbar(
            "settings_scrollbar",
            (screen_size()[0]-40, screen_size()[1]//2),
            (20, screen_size()[1]-30),
            texture=tx.asset("ui/slider.png"),
            splices=tx.data("ui/slider.json")
        ), "scrollbar")

        self.add_object(menu.Button(
            "back_button",
            (150, 50),
            (200, 50),
            texture=tx.asset("ui/button.png"),
            splices=tx.data("ui/button.json"),
            font_size=20, font_color=(255,255,255), text=lang.load_lang('back'), font='Monocraft'
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
        #log_file.write('Settings saved')

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
                    game_menu = MainMenu(screen)
        for slider_text, slider in zip(self.objects['slider_text'], self.objects['slider']):
            slider_text.text = str(slider.value)+'%'
            
class TexturepacksMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "texturepacks_title",
            (screen_size()[0]//2, 50),
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

        y = 50
        texturepacks = ['default'] + os.listdir(tx.get_resource_path(rf"./texturepacks"))
        for texturepack in texturepacks:
            y += 110
            self.add_object(menu.Box(
                "text_" + texturepack,
                (screen_size()[0]//2, y),
                (750, 100),
                texture=tx.asset("ui/box.png"),
                splices=tx.data("ui/box.json")
            ), "box")
            self.add_object(menu.Image(
                "image_" + texturepack,
                (screen_size()[0]//2 - 330, y - 5),
                (80, 80),
                texture=tx.texturepack(pack=texturepack, path='/pack.png')
            ), "image")
            self.add_object(menu.Text(
                "name_" + texturepack,
                (screen_size()[0]//2, y - 26),
                (550, 100),
                text=tx.load_data(tx.texturepack(pack=texturepack, path='/pack.json'))['name'],
                font_color=(255,255,255),
                font_size=24,
                font='Monocraft',
                align='left'
            ), "text")
            self.add_object(menu.Text(
                "author_" + texturepack,
                (screen_size()[0]//2, y - 30),
                (720, 100),
                text=tx.load_data(tx.texturepack(pack=texturepack, path='/pack.json'))['author'],
                font_color=(255,255,255),
                font_size=16,
                font='Monocraft',
                align='right'
            ), "text")
            self.add_object(menu.Text(
                "description_" + texturepack,
                (screen_size()[0]//2, y),
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
            text.draw(screen)
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    global game_menu
                    game_menu = MainMenu(screen)
        for box in self.objects['box']:
            if box.id.startswith('text_'):
                box.value = False
                if box.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                    _settings = settings.get()
                    _settings['texturepack'] = box.id.split('_')[1]
                    settings.save(_settings)
                    #log_file.write("Texturepack set to " + box.id.split('_')[1])

class ModsMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "mods_title",
            (screen_size()[0]//2, 50),
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
                (screen_size()[0]//2, y),
                (750, 100),
                texture=tx.asset("ui/box.png"),
                splices=tx.data("ui/box.json"),
                default=True if mod in settings.get()['mods'] else False
            ), "box")
            self.add_object(menu.Image(
                "image_" + mod,
                (screen_size()[0]//2 - 330, y - 5),
                (80, 80),
                texture=mods.path(mod=mod, path='/mod.png')
            ), "image")
            self.add_object(menu.Text(
                "name_" + mod,
                (screen_size()[0]//2, y - 26),
                (550, 100),
                text=mods.load_data(mods.path(mod=mod, path='/mod.json'))['name'],
                font_color=(255,255,255),
                font_size=24,
                font='Monocraft',
                align='left'
            ), "text")
            self.add_object(menu.Text(
                "author_" + mod,
                (screen_size()[0]//2, y - 30),
                (720, 100),
                text=mods.load_data(mods.path(mod=mod, path='/mod.json'))['author'],
                font_color=(255,255,255), font_size=16, font='Monocraft', align='right'
            ), "text")
            self.add_object(menu.Text(
                "description_" + mod,
                (screen_size()[0]//2, y),
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
            text.draw(screen)
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    global game_menu
                    game_menu = MainMenu(screen)
        for box in self.objects['box']:
            if box.id.startswith('text_'):
                _settings = settings.get()
                if box.value == True and _settings['mods'].count(box.id.split('_')[1]) == 0:
                    _settings['mods'].append(box.id.split('_')[1])
                    settings.save(_settings)
                    #log_file.write("Mod " + box.id.split('_')[1] + " enabled")
                elif box.value == False and _settings['mods'].count(box.id.split('_')[1]) == 1:
                    _settings['mods'].remove(box.id.split('_')[1])
                    settings.save(_settings)
                    #log_file.write("Mod " + box.id.split('_')[1] + " disabled")

class CreditsMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.add_object(menu.Text(
            "credits_title",
            (screen_size()[0]//2, 50),
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
        for line in lang.load_lang("credits.text"):
            y += 50
            self.add_object(menu.Text(
                "credits_text",
                (screen_size()[0]//2, y),
                (200, 30),
                text=line if not line.startswith('-') else line[1:],
                font_color=(255,255,255),
                font_size=40 if not line.startswith('-') else 24,
                font='Monocraft'
            ), "text")
    
    def draw(self):
        self.render()
        for text in self.objects['text']:
            text.draw(screen)
    
    def events(self, event, deltaTime):
        self.update(event)
        for button in self.objects['button']:
            if button.is_hover() and event.type == pygame.MOUSEBUTTONDOWN:
                if button.id == "back_button":
                    global game_menu
                    game_menu = MainMenu(screen)

#log_file.write("All Menus Loaded")
game_menu = LoadingMenu(screen)

def main():
    #log_file.write("Enter Core Loop")
    while True:
        try:
            dt = delta_time(clock, 60)

            screen.fill((100, 100, 100))

            for event in pygame.event.get():
                default_events(event)
                game_menu.events(event, dt)

            game_menu.draw()

            pygame.display.update()
        except Exception as e:
            #log_file.write(f"Exception: {e}", level="ERROR")
            #log_file.write(traceback.format_exc())
            raise e

if __name__ == "__main__":
    main().run()
    #log_file.write("Exiting")
