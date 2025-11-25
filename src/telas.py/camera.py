import pygame
from config import LARGURA_TELA, ALTURA_TELA, LARGURA_MUNDO, ALTURA_MUNDO

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def aplicar(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def aplicar_pos(self, pos):
        return (pos[0] - self.offset.x, pos[1] - self.offset.y)

    def aplicar_fundo(self, fundo_rect):
        # Desloca a camera em relação ao fundo
        return fundo_rect.move(-self.offset.x, -self.offset.y)

    def aplicar_ponto(self, ponto):
        return (ponto[0] - self.offset.x, ponto[1] - self.offset.y)

    def atualizar(self, alvo):
        x_alvo = alvo.posicao_fixa_x
        y_alvo = alvo.posicao_fixa_y

        # Calcula o offset necessário
        x = x_alvo - LARGURA_TELA // 2
        y = y_alvo - ALTURA_TELA // 2

        # Impede a camera de sair do mundo
        x = max(0, min(x, LARGURA_MUNDO - LARGURA_TELA))
        y = max(0, min(y, ALTURA_MUNDO - ALTURA_TELA))

        self.offset.update(x, y)
