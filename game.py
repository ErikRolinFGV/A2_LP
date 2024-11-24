import pygame
import sys

# Classe principal do jogo
class Game:
    def __init__(self):
        # Inicializa o Pygame
        pygame.init()

        # Configuração inicial da janela do jogo
        pygame.display.set_caption("Strongest Slime Ever")  # Título da janela
        self.screen = pygame.display.set_mode((640, 480))  # Define o tamanho da janela
        self.clock = pygame.time.Clock()  # Relógio para controlar a taxa de quadros
        
        # Carregamento e configuração da imagem
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")  # Carrega a imagem
        self.img.set_colorkey((0, 0, 0))  # Define a cor transparente (preto neste caso)
        self.img_pos = [160, 260]  # Posição inicial da imagem
        self.moviment = [False, False]  # Movimentos: [cima, baixo]

        # Área de colisão
        self.collision_area = pygame.Rect(50, 50, 300, 50)  # Retângulo para detectar colisões

    # Método principal para rodar o jogo
    def run(self):
        while True:
            # Preenche a tela com uma cor de fundo (azul claro)
            self.screen.fill((14, 219, 248))

            # Atualiza a posição da imagem de acordo com o movimento
            self.img_pos[1] += (self.moviment[1] - self.moviment[0]) * 5

            # Desenha a imagem na tela na posição atualizada
            self.screen.blit(self.img, self.img_pos)

            # Cria o retângulo da imagem para detecção de colisões
            img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            
            # Verifica colisão entre a imagem e a área de colisão
            if img_rect.colliderect(self.collision_area):
                # Muda a cor da área de colisão se houver interseção
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                # Cor padrão da área de colisão
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            # Processa eventos do teclado e do mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fecha o jogo se clicar para sair
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Quando uma tecla é pressionada
                    if event.key == pygame.K_UP:  # Tecla para mover para cima
                        self.moviment[0] = True
                    if event.key == pygame.K_DOWN:  # Tecla para mover para baixo
                        self.moviment[1] = True
                if event.type == pygame.KEYUP:  # Quando uma tecla é solta
                    if event.key == pygame.K_UP:  # Para o movimento para cima
                        self.moviment[0] = False
                    if event.key == pygame.K_DOWN:  # Para o movimento para baixo
                        self.moviment[1] = False

            # Atualiza a tela com as mudanças feitas
            pygame.display.update()
            
            # Controla a taxa de quadros (60 FPS)
            self.clock.tick(60)

# Instancia e executa o jogo
Game().run()


