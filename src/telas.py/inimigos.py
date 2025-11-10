import pygame, random, math
import config

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        self.image = pygame.Surface((40, 25))
        self.image.fill(config.VERMELHO)
        self.rect = self.image.get_rect()

        # Spawn aleatório fora da tela (bordas do mundo)
        lado = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        if lado == 'cima':
            self.rect.x = random.randint(0, config.LARGURA_MUNDO)
            self.rect.y = -50
        elif lado == 'baixo':
            self.rect.x = random.randint(0, config.LARGURA_MUNDO)
            self.rect.y = config.ALTURA_MUNDO + 50
        elif lado == 'esquerda':
            self.rect.x = -50
            self.rect.y = random.randint(0, config.ALTURA_MUNDO)
        else:
            self.rect.x = config.LARGURA_MUNDO + 50
            self.rect.y = random.randint(0, config.ALTURA_MUNDO)

        # Atributos de comportamento
        self.vel = random.uniform(1.5, 3.0)
        self.jogador = jogador
        self.vida = 1
        self.dano = 1

    def update(self):
        # Persegue o jogador
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.vel
        self.rect.y += dy * self.vel
