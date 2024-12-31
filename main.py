import pygame
import sys
from pycellmachine.cell import Cell
from pycellmachine.grid import Grid


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("PyCellMachine")
        self.clock = pygame.time.Clock()
        self.state = "main_menu"
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # UI Elements
        self.button_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        
        # Cell bar settings
        self.cell_bar_height = 100
        self.cell_bar_scroll = 0
        self.cell_types = ["Basic", "Mover", "Rotator", "Generator"]  # Example cell types
        
        # Grid settings
        self.grid = None

    def run(self):
        while True:
            if self.state == "main_menu":
                self.main_menu()
            elif self.state == "texture_pack":
                self.texture_pack_screen()
            elif self.state == "mod_selection":
                self.mod_selection_screen()
            elif self.state == "sandbox":
                self.sandbox_screen()

    def main_menu(self):
        while self.state == "main_menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check button clicks
                    if self.check_button_click(mouse_pos, "Sandbox", 1):
                        self.state = "sandbox"
                    elif self.check_button_click(mouse_pos, "Texture Packs", 2):
                        self.state = "texture_pack"
                    elif self.check_button_click(mouse_pos, "Mods", 3):
                        self.state = "mod_selection"
                    elif self.check_button_click(mouse_pos, "Exit", 4):
                        pygame.quit()
                        sys.exit()

            self.screen.fill(self.BLACK)
            
            # Draw title
            title = self.title_font.render("PyCellMachine", True, self.WHITE)
            self.screen.blit(title, (640 - title.get_width()//2, 100))
            
            # Draw buttons
            self.draw_menu_button("Sandbox", 1)
            self.draw_menu_button("Texture Packs", 2)
            self.draw_menu_button("Mods", 3)
            self.draw_menu_button("Exit", 4)
            
            pygame.display.flip()
            self.clock.tick(60)

    def sandbox_screen(self):
        if not self.grid:
            self.grid = pcm.Grid(100, 100)
        
        selected_cell_type = 0
        
        while self.state == "sandbox":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Handle cell placement
                    if mouse_pos[1] < 720 - self.cell_bar_height:
                        grid_pos = self.grid.get_grid_coordinates(*mouse_pos)
                        if self.grid.is_within_bounds(*grid_pos):
                            new_cell = pcm.Cell(*grid_pos, grid=self.grid)
                            self.grid.add_cell(new_cell)
                    # Handle cell bar scrolling and selection
                    elif mouse_pos[1] >= 720 - self.cell_bar_height:
                        if event.button == 4:  # Mouse wheel up
                            self.cell_bar_scroll = max(0, self.cell_bar_scroll - 1)
                        elif event.button == 5:  # Mouse wheel down
                            self.cell_bar_scroll = min(len(self.cell_types) - 5, self.cell_bar_scroll + 1)
                        else:
                            selected_cell_type = self.get_selected_cell_type(mouse_pos[0])

            self.screen.fill(self.BLACK)
            
            # Draw grid
            for cell in self.grid.cells.values():
                screen_pos = cell.get_screen_position()
                pygame.draw.rect(self.screen, self.WHITE, 
                               (screen_pos[0], screen_pos[1], self.grid.scale, self.grid.scale))
            
            # Draw cell selection bar
            self.draw_cell_bar(selected_cell_type)
            
            pygame.display.flip()
            self.clock.tick(60)

    def texture_pack_screen(self):
        while self.state == "texture_pack":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_button_click(pygame.mouse.get_pos(), "Back", 1):
                        self.state = "main_menu"

            self.screen.fill(self.BLACK)
            self.draw_menu_button("Back", 1)
            pygame.display.flip()
            self.clock.tick(60)

    def mod_selection_screen(self):
        while self.state == "mod_selection":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_button_click(pygame.mouse.get_pos(), "Back", 1):
                        self.state = "main_menu"

            self.screen.fill(self.BLACK)
            self.draw_menu_button("Back", 1)
            pygame.display.flip()
            self.clock.tick(60)

    def draw_menu_button(self, text, position):
        button = self.button_font.render(text, True, self.WHITE)
        button_rect = button.get_rect(center=(640, 250 + position * 70))
        self.screen.blit(button, button_rect)
        return button_rect

    def check_button_click(self, mouse_pos, text, position):
        button_rect = self.button_font.render(text, True, self.WHITE).get_rect(center=(640, 250 + position * 70))
        return button_rect.collidepoint(mouse_pos)

    def draw_cell_bar(self, selected):
        pygame.draw.rect(self.screen, self.GRAY, (0, 720 - self.cell_bar_height, 1280, self.cell_bar_height))
        
        cell_width = 100
        for i, cell_type in enumerate(self.cell_types[self.cell_bar_scroll:self.cell_bar_scroll + 8]):
            x = i * cell_width + 10
            color = self.WHITE if i == selected else self.BLACK
            pygame.draw.rect(self.screen, color, (x, 720 - self.cell_bar_height + 10, 80, 80))
            cell_name = self.button_font.render(cell_type, True, self.BLACK if i == selected else self.WHITE)
            self.screen.blit(cell_name, (x + 40 - cell_name.get_width()//2, 720 - 30))

    def get_selected_cell_type(self, x):
        return (x // 100) if 0 <= x < 800 else -1

if __name__ == "__main__":
    game = Game()
    game.run()
