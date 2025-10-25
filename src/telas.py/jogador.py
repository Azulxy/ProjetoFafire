import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela // 2, altura_tela - 50)
        self.vel = 5
        self.largura_tela = largura_tela

    def update(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if teclas[pygame.K_UP]:
            self.rect.y -= 5
        if teclas[pygame.K_DOWN]:
            self.rect.y += 5

        # Impedir que saia da tela
        self.rect.x = max(0, min(self.rect.x, self.largura_tela - self.rect.width))
