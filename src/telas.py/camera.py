import pygame
from config import LARGURA_TELA, ALTURA_TELA, LARGURA_MUNDO, ALTURA_MUNDO

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def aplicar(self, entidade):
        if isinstance(entidade, pygame.Rect):
            return entidade.move(-self.offset.x, -self.offset.y)
        return entidade.rect.move(-self.offset.x, -self.offset.y)


    def aplicar_fundo(self, fundo_rect):
        # Desloca a camera em relação ao fundo
        return fundo_rect.move(-self.offset.x, -self.offset.y)

    def atualizar(self, alvo):
        # Centraliza a camera no jogador
        x = alvo.rect.centerx - LARGURA_TELA / 2
        y = alvo.rect.centery - ALTURA_TELA / 2

        # Impede a camera de sair do mundo
        x = max(0, min(x, LARGURA_MUNDO - LARGURA_TELA))
        y = max(0, min(y, ALTURA_MUNDO - ALTURA_TELA))

        self.offset.update(x, y)
