import pygame
import sys
from src import menu

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
        self.menu.add_object(menu.Button(
            "exit_button",
            (300, 300),
            (200, 30),
            color=[(100,100,100),(50,50,50)],
            text_size=20, font_color=(255,255,255), text='Leave Game', font='Arial'
        ), "button")
    def draw(self):
        self.menu.draw()
    def events(self):
        for button in self.menu.objects['button']:
            if button.is_clicked():
                if button.id == "exit_button":
                    pygame.quit()
                    sys.exit()

game_menu = MainMenu()

def main():
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            default_events(event)
            game_menu.events()
        
        game_menu.draw()
        pygame.display.update()

        dt = delta_time(clock, 60)

if __name__ == "__main__":
    game = main()
    game.run()
