import random

class Cloud:
    """
    A class to represent a cloud in a 2D environment.
    Attributes:
    ----------
    pos : list
        The position of the cloud as a list [x, y].
    img : pygame.Surface
        The image representing the cloud.
    speed : float
        The speed at which the cloud moves horizontally.
    depth : float
        The depth factor for parallax scrolling.
    Methods:
    -------
    update():
        Updates the position of the cloud based on its speed.
    render(surf, offset=(0, 0)):
        Renders the cloud on the given surface with an optional offset for parallax scrolling.
    """
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed
        
    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))
        
class Clouds:
    """
    A class to represent a collection of clouds in a 2D space.
    Attributes:
    ----------
    clouds : list
        A list to store individual cloud objects.
    Methods:
    -------
    __init__(cloud_images, count=16):
        Initializes the Clouds object with a specified number of clouds.
    update():
        Updates the state of each cloud in the collection.
    render(surf, offset=(0, 0)):
        Renders each cloud onto a given surface with an optional offset.
    """
    def __init__(self, cloud_images, count=16):
        self.clouds = []
        
        for i in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
        
        self.clouds.sort(key=lambda x: x.depth)
    
    def update(self):
        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)



        