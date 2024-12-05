import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    """
    A class to represent an animation sequence.
    Attributes:
    -----------
    images : list
        A list of images that make up the animation.
    loop : bool
        A flag to determine if the animation should loop.
    img_duration : int
        The duration each image is displayed for.
    done : bool
        A flag to indicate if the animation is done (used when loop is False).
    frame : int
        The current frame of the animation.
    Methods:
    --------
    __init__(images, img_dur=5, loop=True):
        Initializes the Animation object with images, image duration, and loop flag.
    copy():
        Returns a copy of the current Animation object.
    update():
        Updates the current frame of the animation. If looping, it wraps around. If not looping, it stops at the last frame.
    img():
        Returns the current image to be displayed based on the current frame.
    """
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]