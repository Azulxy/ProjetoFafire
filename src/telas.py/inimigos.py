import pygame
import random
import math
import config
import os

SPRITE_SHEET_PATH = "assets/imagens/Inimigo_Sprite_Sheet.png"
SCALE_INIMIGO = 0.8 

# --- CONFIGURAÇÃO MANUAL DO RECT ---
# Defina o tamanho que a caixa de colisão DEVE TER (em pixels APÓS a escala).
# Se o seu SCALE_INIMIGO é 2.0 e o peixe original tem 20x20, ele terá 40x40.
# Um rect de 30x30 seria 30x30 pixels.
RECT_WIDTH = 70
RECT_HEIGHT = 70
# ------------------------------------

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador, vel_bonus=0):
        super().__init__()

        self.jogador = jogador
        
        # --- 1. CARREGAMENTO E ESCALA DA IMAGEM ---
        w_fallback, h_fallback = 40, 40
        fallback_image = pygame.Surface((w_fallback, h_fallback), pygame.SRCALPHA).convert_alpha()
        fallback_image.fill((255, 0, 0))
        
        self.original_image = fallback_image 

        try:
            image_base = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()
            
            original_w, original_h = image_base.get_size()
            w = int(original_w * SCALE_INIMIGO)
            h = int(original_h * SCALE_INIMIGO)
            
            self.original_image = pygame.transform.scale(image_base, (w, h))

        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem do inimigo em {SPRITE_SHEET_PATH}: {e}. Usando fallback (Quadrado Vermelho).")
        
        
        self.image = self.original_image
        
        # --- AJUSTE: CRIA O RECT MENOR NO CENTRO ---
        # Cria um rect do tamanho da imagem, depois ajusta o tamanho para o desejado
        temp_rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, RECT_WIDTH, RECT_HEIGHT)
        self.rect.center = temp_rect.center # Centraliza o rect menor na imagem
        # --------------------------------------------
        
        self.virado_esquerda = False
        self.vel = random.uniform(1.8, 2.2) + vel_bonus

        # POSIÇÃO INICIAL (Lógica de spawn fora da tela)
        lado = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        if lado == "cima":
            self.rect.x = random.randint(0, config.LARGURA_MUNDO - self.rect.width)
            self.rect.y = -self.rect.height
        elif lado == "baixo":
            self.rect.x = random.randint(0, config.LARGURA_MUNDO - self.rect.width)
            self.rect.y = config.ALTURA_MUNDO
        elif lado == "esquerda":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, config.ALTURA_MUNDO - self.rect.height)
        else:
            self.rect.x = config.LARGURA_MUNDO
            self.rect.y = random.randint(0, config.ALTURA_MUNDO - self.rect.height)
            
        # Posição FLOAT para movimento suave
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
            
        self.direction = pygame.math.Vector2(0, 0)
        
        # Flag de debug
        self.debug_rect = False


    def update(self):
        
        # 1. CÁLCULO DA DIREÇÃO (Movimento em Linha Reta)
        dx = self.jogador.rect.centerx - self.x
        dy = self.jogador.rect.centery - self.y
        dist = math.hypot(dx, dy)
        
        # Posição antes da rotação (para manter o sprite no lugar)
        current_center = self.rect.center 
        
        # Aplicação do movimento
        if dist > 0:
            self.direction.x = dx / dist
            self.direction.y = dy / dist
            
            # Aplicar no FLOAT
            self.x += self.direction.x * self.vel
            self.y += self.direction.y * self.vel
            
            # Aplicar no RECT (Pygame usa int)
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        elif dist == 0:
            self.direction = pygame.math.Vector2(0, 0)

        # 2. ROTAÇÃO E FLIP
        base_image = self.original_image
        
        if self.direction.x < 0.0:
            self.virado_esquerda = True
        elif self.direction.x > 0.0:
            self.virado_esquerda = False

        if self.virado_esquerda:
             base_image = pygame.transform.flip(self.original_image, True, False)

        if self.virado_esquerda:
            angle = -math.degrees(math.atan2(-self.direction.y, abs(self.direction.x) if abs(self.direction.x) > 0.001 else 0.001))
        else:
            angle = -math.degrees(math.atan2(self.direction.y, self.direction.x) if abs(self.direction.x) > 0.001 else -math.degrees(math.atan2(self.direction.y, 0.001)))
        
        # Aplica a rotação e corrige o rect no novo centro
        self.image = pygame.transform.rotate(base_image, angle)
        
        # RECRIA O RECT, MANTENDO O CENTRO JÁ ATUALIZADO PELO MOVIMENTO
        new_center = self.rect.center
        
        # CRIA UM RECT DO TAMANHO DA IMAGEM ROTACIONADA
        rotated_image_rect = self.image.get_rect(center=new_center)
        
        # RECria o RECT DA COLISÃO (menor) e o posiciona no centro
        self.rect = pygame.Rect(0, 0, RECT_WIDTH, RECT_HEIGHT)
        self.rect.center = rotated_image_rect.center # Usa o centro da imagem rotacionada
        
        # --- DEBUG: DESENHAR BORDA DO RECT ---
        if self.debug_rect:
            # Cria uma superfície transparente para desenhar a borda
            debug_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            
            # Desenha o retangulo (borda) no tamanho e posição do nosso self.rect (caixa de colisão)
            # A posição é ajustada para o offset da imagem atual
            debug_rect_no_sprite = self.rect.copy()
            debug_rect_no_sprite.topleft = (self.rect.x - rotated_image_rect.x, self.rect.y - rotated_image_rect.y)
            
            pygame.draw.rect(debug_surface, (255, 0, 0), debug_rect_no_sprite, 1) # Borda vermelha
            
            # Combina a imagem do inimigo com a superfície de debug
            self.image.blit(debug_surface, (0, 0))