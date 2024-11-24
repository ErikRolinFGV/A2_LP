import pygame

import os

IMG_PATH_BASE = 'data/images/'

def load_image(path):
    img = pygame.image.load(IMG_PATH_BASE + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(IMG_PATH_BASE + path)):
        images.append(load_image(path + '/' + img_name))
    
    return images