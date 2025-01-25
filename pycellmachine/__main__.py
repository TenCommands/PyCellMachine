import pygame
#pygame.init()
import sys, os, json, traceback
from pycellmachine._internal import menu
from pycellmachine._internal import textures as tx
from pycellmachine._internal import settings
from pycellmachine._internal import mods
import pycellmachine._internal.menus as menus

#appicon = pygame.image.load(r'./_internal/assets/logo.png')
pygame.display.set_caption('PyCellMachine')
#pygame.display.set_icon(appicon)

global game_menu
game_menu = None

global screen
screen = pygame.display.set_mode(menu.display_size(), pygame.RESIZABLE)

clock = pygame.time.Clock()

def delta_time(clock_obj, frame_rate):
    return clock_obj.tick(frame_rate) / 1000.0

def default_events(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()

game_menu = menus.LoadingMenu(screen)

def main():
    while True:
        dt = delta_time(clock, 60)

        screen.fill((100, 100, 100))

        for event in pygame.event.get():
            default_events(event)
            game_menu.events(event, dt)
        
        game_menu.draw()
        
        pygame.display.update()

if __name__ == "__main__":
    main().run()