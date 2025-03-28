import pygame, json, numpy as math, sys
from . import api

pygame.display.set_caption('PyCellMachine')

global game_menu
game_menu = None

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

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

def main():

    grid = api.Grid(10,6, scale=5)

    cells = api.__all_cells__
    grid.add_cell(cells['ten.default.mover']((0, 0), (1, 0)))
    grid.add_cell(cells['ten.default.push']((4, 0), (1, 0)))
    grid.add_cell(cells['ten.default.generator']((4, 1), (0, -1)))
    grid.add_cell(cells['ten.default.slider']((5, 2), (1, 0)))
    grid.add_cell(cells['ten.default.push']((5, 5), (1, 0)))
    grid.add_cell(cells['ten.default.generator']((5, 4), (0, 1)))
    grid.add_cell(cells['ten.default.slider']((4, 3),(0, 1)))
    grid.add_cell(cells['ten.default.generator']((3, 0), (-1, 0)))
    grid.add_cell(cells['ten.default.generator']((6, 5), (1, 0)))

    while True:
        dt = delta_time(clock, 60)
        screen.fill((100, 100, 100))
        for event in pygame.event.get():
            default_events(event)
            grid.events(event)
        grid.tick()
        grid.draw(screen)
        pygame.display.update()
        clock.tick(60)
    
if __name__ == '__main__':
    main()

