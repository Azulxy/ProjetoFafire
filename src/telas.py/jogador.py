import pygame
import config

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 5
        self.direcao = "direita"
        self.largura_mundo = config.LARGURA_MUNDO
        self.altura_mundo = config.ALTURA_MUNDO

    def update(self, teclas):
        # Movimento
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
            self.direcao = "esquerda"
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel
            self.direcao = "direita"
        if teclas[pygame.K_UP]:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.vel

        # Limites do mundo
        self.rect.x = max(0, min(self.rect.x, self.largura_mundo - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.altura_mundo - self.rect.height))
