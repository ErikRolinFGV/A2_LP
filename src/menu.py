import pygame
from src.util import load_image
print(pygame.version.ver)
class Menu:
    """
    A class to represent the game menu.
    Attributes
    ----------
    screen : pygame.Surface
        The main screen surface where the menu will be rendered.
    display : pygame.Surface
        The display surface where the menu image will be initially rendered.
    assets : dict
        A dictionary containing game assets.
    menu_image : pygame.Surface
        The image used for the menu background.
    Methods
    -------
    render():
        Renders the menu on the screen.
    """
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

