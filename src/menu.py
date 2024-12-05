import pygame
from src.util import load_image

class Menu:
    def __init__(self, screen, display, assets):
        self.screen = screen
        self.display = display
        self.assets = assets
        self.menu_image = load_image("menu_jogo.jpg")

    def render(self):
        # Scale the menu image to fit the display surface
        scaled_menu_image = pygame.transform.scale(self.menu_image, self.display.get_size())
        self.display.blit(scaled_menu_image, (0, 0))

        # Scale the display surface to fit the screen surface
        scaled_display = pygame.transform.scale(self.display, self.screen.get_size())
        self.screen.blit(scaled_display, (0, 0))
        pygame.display.update()