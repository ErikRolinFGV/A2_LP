import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        # Calcular a posição de renderização levando em conta a profundidade (depth)
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)

        # Corrigido o erro de sintaxe e ajustado para permitir a rotação da imagem (repetição na tela)
        surface.blit(self.img, (
            render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(),
            render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()
        ))


class Clouds: 
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            # Geração das posições aleatórias dentro de uma área mais controlada
            x_pos = random.random() * 999  # Limitando a posição X (ex: até 999)
            y_pos = random.random() * 999  # Limitando a posição Y (ex: até 999)
            
            self.clouds.append(Cloud(
                (x_pos, y_pos),  # A posição agora é mais controlada
                random.choice(cloud_images),  # Escolhendo uma imagem aleatória para a nuvem
                random.random() * 0.05 + 0.05,  # Velocidade aleatória
                random.random() * 0.6 + 0.2  # Profundidade aleatória
            ))
        
        # Organizando as nuvens por profundidade (para renderizar as mais distantes primeiro)
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        # Atualiza todas as nuvens
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        # Renderiza todas as nuvens na tela
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)



        