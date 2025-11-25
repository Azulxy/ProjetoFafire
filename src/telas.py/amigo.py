import pygame

SCALE_AMIGO = 0.7

class Amigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        base_w, base_h = 40, 40
        w = int(base_w * SCALE_AMIGO)
        h = int(base_h * SCALE_AMIGO)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # placeholder verde — substitua pelo seu sprite (mesmo tamanho) quando tiver
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(center=(x, y))