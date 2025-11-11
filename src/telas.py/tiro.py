import pygame
import math
from config import VERMELHO

class Tiro(pygame.sprite.Sprite):
    def __init__(self, pos_origem, pos_alvo, velocidade=6):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(center=pos_origem)

        dx = pos_alvo[0] - pos_origem[0]
        dy = pos_alvo[1] - pos_origem[1]
        distancia = math.hypot(dx, dy)
        if distancia == 0:
            distancia = 1
        self.vel_x = dx / distancia * velocidade
        self.vel_y = dy / distancia * velocidade

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Remover se sair da tela
        if (self.rect.right < 0 or self.rect.left > 2000 or 
            self.rect.bottom < 0 or self.rect.top > 2000):
            self.kill()
