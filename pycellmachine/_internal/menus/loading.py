import pygame
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
import pycellmachine._internal.menus as menus

class LoadingMenu(menu.Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.loading_image = pygame.image.load(tx.get_resource_path(r'.\_internal\assets\title.png'))
    
    def draw(self):
        if pygame.time.get_ticks() / 1000 > 5:
            # fade out self.loading_image by alpha
            self.loading_image.set_alpha(255 - (pygame.time.get_ticks() / 1000 - 5) * 255)
            if pygame.time.get_ticks() / 1000 > 6:
                global game_menu
                game_menu = menus.MainMenu(self.screen)
        else: 
            self.loading_image.set_alpha(pygame.time.get_ticks() / 1500 * 255)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.loading_image, (menu.screen_size()[0]//2 - self.loading_image.get_width()//2, menu.screen_size()[1]//2 - self.loading_image.get_height()//2))
    
    def events(self, event, deltaTime):
        self.update(event)