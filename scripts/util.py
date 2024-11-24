import pygame

IMG_PATH_BASE = 'data/images/'

def load_image(path):
    img = pygame.image.load(IMG_PATH_BASE + path).convert()
    img.set_colorkey((0, 0, 0))
    return img