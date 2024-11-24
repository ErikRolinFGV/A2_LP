import pygame

class Physics:
    def __init__(self, game, ent_type, pos, size):
        self.game = game  # Referência ao jogo principal
        self.type = ent_type  # Tipo da entidade
        self.pos = list(pos)  # Posição inicial (lista para mutabilidade)
        self.size = size  # Tamanho da entidade (largura, altura)
        self.velocity = [0, 0]  # Velocidade (X, Y)

    def rect(self):
        # Retorna o retângulo atual da entidade com base na posição e no tamanho
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        # Calcula o movimento no quadro atual (movimento + velocidade)
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Aplica gravidade no eixo Y (com limite de velocidade)
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Movimento horizontal (X)
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_collision(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:  # Colisão à direita
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:  # Colisão à esquerda
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x  # Atualiza a posição X com base na colisão

        # Movimento vertical (Y)
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_collision(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # Colisão no chão
                    entity_rect.bottom = rect.top
                    self.velocity[1] = 0  # Anula a velocidade vertical ao tocar o chão
                if frame_movement[1] < 0:  # Colisão no teto
                    entity_rect.top = rect.bottom
                    self.velocity[1] = 0  # Anula a velocidade vertical ao bater no teto
                self.pos[1] = entity_rect.y  # Atualiza a posição Y com base na colisão

    def render(self, surface, offset=(0, 0)):
        # Renderiza a entidade na tela
        surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
      