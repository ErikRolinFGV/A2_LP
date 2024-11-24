import pygame
import sys

from scripts.entities import Physics
from scripts.util import load_image, load_images
from scripts.tilemap import tilemap
from scripts.clouds import Clouds


# Classe principal do jogo
class Game:
    def __init__(self):
        # Inicializa o Pygame
        pygame.init()

        # Configuração inicial da janela do jogo
        pygame.display.set_caption("Strongest Slime Ever")  # Título da janela

        self.screen = pygame.display.set_mode((640, 480))  # Define o tamanho da janela
        
        self.clock = pygame.time.Clock()  # Relógio para controlar a taxa de quadros

        self.display = pygame.Surface((320, 240))


        self.assets = {
            'player': load_image('entities/player.png'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'decor' : load_images('tiles/decor'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds')
            
        }

        print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Physics(self, "player", (50, 50), (8, 15))

        self.moviment = [False, False]

        self.tilemap = tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    # Método principal para rodar o jogo
    def run(self):
        while True:
            # Preenche a tela com uma cor de fundo (azul claro)
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]) )

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=self.scroll)

            self.player.update(self.tilemap, (self.moviment[1]- self.moviment[0], 0))
            self.player.render(self.display, offset=self.scroll)


            print(self.tilemap.physics_rects_collision(self.player.pos))
            # Processa eventos do teclado e do mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fecha o jogo se clicar para sair
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Quando uma tecla é pressionada
                    if event.key == pygame.K_LEFT:  # Tecla para mover para cima
                        self.moviment[0] = True
                    if event.key == pygame.K_RIGHT:  # Tecla para mover para baixo
                        self.moviment[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -2.5
                if event.type == pygame.KEYUP:  # Quando uma tecla é solta
                    if event.key == pygame.K_LEFT:  # Para o movimento para cima
                        self.moviment[0] = False
                    if event.key == pygame.K_RIGHT:  # Para o movimento para baixo
                        self.moviment[1] = False


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            # Atualiza a tela com as mudanças feitas
            pygame.display.update()
            
            # Controla a taxa de quadros (60 FPS)
            self.clock.tick(60)

# Instancia e executa o jogo
Game().run()


