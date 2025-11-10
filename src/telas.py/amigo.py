import pygame

class Amigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))