import pygame
import math
import random

from src.particle import Particle

class PhysicsEntity:
    """
    A class to represent a physics-based entity in a game.
    Attributes:
    -----------
    game : object
        The game instance to which this entity belongs.
    type : str
        The type of the entity.
    pos : list
        The position of the entity as a list [x, y].
    size : tuple
        The size of the entity as a tuple (width, height).
    velocity : list
        The velocity of the entity as a list [vx, vy].
    collisions : dict
        A dictionary indicating collision status in four directions.
    action : str
        The current action of the entity.
    anim_offset : tuple
        The offset for the animation as a tuple (x_offset, y_offset).
    flip : bool
        A flag indicating whether the entity's image should be flipped horizontally.
    last_movement : list
        The last movement vector of the entity.
    Methods:
    --------
    rect():
        Returns the pygame.Rect object representing the entity's position and size.
    set_action(action):
        Sets the current action of the entity and updates the animation.
    update(tilemap, movement=(0, 0)):
        Updates the entity's position, handles collisions, and updates the animation.
    render(surf, offset=(0, 0)):
        Renders the entity on the given surface with an optional offset.
    """
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        
        self.last_movement = [0, 0]
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        """
        Update the entity's position and handle collisions with the tilemap.
        Args:
            tilemap: The tilemap containing the physics rectangles for collision detection.
            movement (tuple): A tuple representing the movement vector (dx, dy).
        Updates:
            - Adjusts the entity's position based on the movement and velocity.
            - Checks for collisions with the tilemap and adjusts the position accordingly.
            - Updates the entity's collision status (up, down, right, left).
            - Flips the entity's orientation based on the horizontal movement direction.
            - Updates the entity's velocity, applying gravity.
            - Resets vertical velocity if a collision occurs on the top or bottom.
            - Updates the entity's animation state.
        """
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        """
        Updates the entity's state based on the tilemap and movement.
        Args:
            tilemap: The tilemap to check for collisions and solid tiles.
            movement (tuple): A tuple representing the movement in the x and y directions.
        Returns:
            bool: True if the entity collides with the player while the player is dashing, otherwise None.
        """
        if self.walking:
            if tilemap.solid_tile_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if self.collisions['right'] or self.collisions['left']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            
            if not self.walking:
                dist_to_player = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dist_to_player[1]) < 16):
                    if (self.flip and dist_to_player[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                    if (not self.flip and dist_to_player[0] > 0):
                         self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                       
        elif random.random() < 0.01:  # 1% chance of changing direction
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                return True

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets["gun"], True, False), (self.rect().centerx - 4 - self.game.assets["gun"].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets["gun"], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    """
    Player class represents a player entity in the game, inheriting from PhysicsEntity.
    It handles player-specific mechanics such as jumping, dashing, wall sliding, and updating the player's state.
        air_time (int): The amount of time the player has been in the air.
        jumps (int): The number of jumps the player has left.
        wall_slide (bool): Indicates if the player is currently wall sliding.
        dashing (int): The current dash state of the player.
        jump_sound (Sound): The sound effect played when the player jumps.
        dash_sound (Sound): The sound effect played when the player dashes.
    Methods:
        __init__(game, pos, size):
            Initializes the player with the given game, position, and size.
        update(tilemap, movement=(0, 0)):
            Updates the player's state based on the tilemap and movement.
        render(surf, offset=(0, 0)):
            Renders the player on the given surface with an optional offset.
        jump():
            Handles the jump mechanics for the player.
        dash():
            Performs a dash action for the player.
    """
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.jump_sound = pygame.mixer.Sound('data/sfx/jump.wav')
        self.dash_sound = pygame.mixer.Sound('data/sfx/dash.wav')

    
    def update(self, tilemap, movement=(0, 0)):
        """
        Updates the entity's state based on the tilemap and movement.
        Args:
            tilemap: The current tilemap of the game.
            movement (tuple): A tuple representing the movement in the x and y directions.
        Updates the following attributes:
            - air_time: Increases by 1 each update. If greater than 360, sets the game state to dead.
            - collisions['down']: Resets air_time to 0 and sets jumps to 1 if there is a collision below.
            - wall_slide: Sets to True if there is a collision on the right or left and air_time is greater than 4.
            - velocity: Adjusts the vertical velocity during a wall slide and horizontal velocity during dashing.
            - flip: Determines the direction the entity is facing during a wall slide.
            - action: Sets the entity's action to 'wall_slide', 'jump', 'run', or 'idle' based on conditions.
            - dashing: Decreases or increases the dashing value and adjusts velocity accordingly.
            - particles: Adds particle effects during dashing.
        """
        super().update(tilemap, movement=movement)
        
        self.air_time += 1

        if self.air_time > 360:
            self.game.dead = 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
            
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
                pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity))

        if abs(self.dashing) in {60 , 50}:
            for i in range(10):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 1
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity))

                
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surf, offset=(0, 0)):
            super().render(surf, offset=offset)


    def jump(self):
        """
        Handles the jump mechanics for the entity.
        If the entity is wall sliding, it will perform a wall jump based on the direction of the last movement.
        If the entity is not wall sliding and has jumps remaining, it will perform a regular jump.
        Returns:
            bool: True if the jump was performed, False otherwise.
        """
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            self.jump_sound.play()
            return True
        
    def dash(self):
        """
        Perform a dash action for the entity.

        If the entity is not already dashing, it will initiate a dash in the
        direction it is currently facing. The dash distance is determined by
        the `flip` attribute. If `flip` is True, the entity will dash to the
        left; otherwise, it will dash to the right. The dash sound effect is
        played when the dash is initiated.

        Attributes:
            dashing (int): The current dash state of the entity. A positive
                           value indicates a dash to the right, and a negative
                           value indicates a dash to the left.
            flip (bool): Indicates the direction the entity is facing. If True,
                         the entity is facing left; otherwise, it is facing right.
            dash_sound (Sound): The sound effect to play when the entity dashes.
        """
        if not self.dashing:
            if self.flip:
                self.dashing = -60
                self.dash_sound.play()
            else:
                self.dashing = 60
                self.dash_sound.play()
