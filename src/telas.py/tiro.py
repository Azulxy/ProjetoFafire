import pygame
import config

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        self.image = pygame.Surface((8, 4))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 10
        self.direcao = direcao

    def update(self):
        self.rect.x += self.vel * self.direcao
        if self.rect.x < 0 or self.rect.x > config.LARGURA_MUNDO:
            self.kill()