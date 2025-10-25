import pygame
from config import LARGURA_TELA, ALTURA_TELA, LARGURA_MUNDO, ALTURA_MUNDO

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def aplicar(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def atualizar(self, alvo):
        self.offset.x = max(0, min(alvo.rect.centerx - LARGURA_TELA / 2, LARGURA_MUNDO - LARGURA_TELA))
        self.offset.y = max(0, min(alvo.rect.centery - ALTURA_TELA / 2, ALTURA_MUNDO - ALTURA_TELA))
