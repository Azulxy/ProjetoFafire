import pygame, random, math
from config import LARGURA_MUNDO, ALTURA_MUNDO, VERMELHO

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        self.image = pygame.Surface((40, 25))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()

        # spawn aleatório fora da tela (nas bordas)
        lado = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        if lado == 'cima':
            self.rect.x = random.randint(0, LARGURA_MUNDO)
            self.rect.y = -50
        elif lado == 'baixo':
            self.rect.x = random.randint(0, LARGURA_MUNDO)
            self.rect.y = ALTURA_MUNDO + 50
        elif lado == 'esquerda':
            self.rect.x = -50
            self.rect.y = random.randint(0, ALTURA_MUNDO)
        else:
            self.rect.x = LARGURA_MUNDO + 50
            self.rect.y = random.randint(0, ALTURA_MUNDO)

        self.vel = 2
        self.jogador = jogador

    def update(self):
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.vel
        self.rect.y += dy * self.vel
