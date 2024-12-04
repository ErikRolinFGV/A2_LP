import sys
import random
import math

import pygame

from scripts.util import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('??')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.possible_scores = [50,60,70,80,90,100]
        self.points = 0
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            "enemy/idle": Animation(load_images("entities/enemy/idle"), img_dur=6),
            "enemy/run": Animation(load_images("entities/enemy/run"), img_dur=4),
            "particles/leaf": Animation(load_images('particles/leaf'), img_dur=40, loop=False),
            "particles/particle": Animation(load_images('particles/particle'), img_dur=6, loop=False) ,
            "gun": load_image("gun.png"),
            "projectile": load_image("projectile.png")
        }
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 1
        self.load_game_level(self.level)
        #Add level spawner (4:43)

    def load_game_level(self, map_id):
            self.tilemap.load("data/maps/" + str(map_id) + ".json")

            self.leaf_spawners = []
            for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
                self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 16, 16))
            print(self.leaf_spawners)
            
            self.enemies = []
            for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
                if spawner["variant"] == 0:
                    self.player.pos = spawner["pos"]
                else:
                    print(spawner["pos"], "enemy")
                    self.enemies.append(Enemy(self, spawner["pos"], (8, 15)))

           


            self.projectiles = []
            self.particles = []

            self.scroll = [0, 0]
            self.dead = 0
        
        
    def run(self):
        while True: 
            self.display.blit(self.assets['background'], (0, 0))

            if not len(self.enemies):
                self.level += 1
                self.load_game_level(self.level)
            
            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_game_level(self.level)
                    self.points = 0
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 10000 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[random.random() * 2 - 1, random.random() * 2 - 1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                    self.points += random.choice(self.possible_scores)
                    print(self.points)

            if not self.dead:  
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # [[x,y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets["projectile"]
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 -render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_tile_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:  # that makes the player invincible when dashing
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1


            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.p_type == "leaf":
                    particle.pos[0] += math.sin(particle.pos[1] / 10) * 0.5
                if kill:
                    self.particles.remove(particle)

            self.font = pygame.font.Font(None, 24)
            score_text = self.font.render(f"Pontuação: {self.points}", True, (255, 255, 255))
            self.display.blit(score_text, (10, 10))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()


