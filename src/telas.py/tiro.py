import pygame
import math
from config import VERMELHO, LARGURA_MUNDO, ALTURA_MUNDO # Importar as dimensões do mundo

class Tiro(pygame.sprite.Sprite):
    def __init__(self, pos_origem, pos_alvo, velocidade=6):
        super().__init__()
        
        # --- Carregar Imagem do Tiro ---
        self.image = pygame.image.load("assets/imagens/tiro.png").convert_alpha()
        
        # --- NOVO: Aumentar a escala da imagem ---
        escala = 0.6
        nova_largura = int(self.image.get_width() * escala)
        nova_altura = int(self.image.get_height() * escala)
        self.image = pygame.transform.scale(self.image, (nova_largura, nova_altura))
        
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

        # Remover se sair das bordas do MUNDO
        if (self.rect.right < 0 or self.rect.left > LARGURA_MUNDO or 
            self.rect.bottom < 0 or self.rect.top > ALTURA_MUNDO):
            self.kill()