import pygame

class Physics:
    def __init__(self, game, ent_type, pos, size):
        self.game = game
        self.type = ent_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=(0,0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surfice):
        surfice.blit(self.game.assets['player'], self.pos)        