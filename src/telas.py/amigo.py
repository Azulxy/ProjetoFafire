import pygame
import math

SCALE_AMIGO = 1.0
AMIGO_PATH = "assets/imagens/amigo.png"

class Amigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.original_image_loaded = pygame.image.load(AMIGO_PATH).convert_alpha()
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem em {AMIGO_PATH}: {e}")
            w, h = 50, 50
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.image.fill((200, 0, 0))
            self.rect = self.image.get_rect(center=(x, y))
            self.pos = pygame.math.Vector2(x, y)
            self.direction = pygame.math.Vector2(1, 0)
            self.virado_esquerda = False
            return

        original_w, original_h = self.original_image_loaded.get_size()
        w = int(original_w * SCALE_AMIGO)
        h = int(original_h * SCALE_AMIGO)
        
        self.original_image = pygame.transform.scale(self.original_image_loaded, (w, h))
        self.image = self.original_image

        self.pos = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(1, 0)
        self.angle = 0
        self.virado_esquerda = False
        
        self.rect = self.image.get_rect(center=self.pos)
        
    def get_left_mid_point(self):
        return self.pos.x, self.pos.y

    def update(self, player_pos):
        # A direção é o vetor do Amigo para o Player (Target - Self)
        target_direction = player_pos - self.pos
        
        if target_direction.length_squared() > 0:
            self.direction = target_direction.normalize()
        else:
            # Não altera a direção se o Amigo estiver na mesma posição do Player
            pass 

        self.rotacionar()

    def rotacionar(self):
        center = self.pos
        
        base_image = self.original_image
        
        # 1. Determina o flip e a imagem base
        if self.direction.x < 0.0:
            self.virado_esquerda = True
        elif self.direction.x > 0.0:
            self.virado_esquerda = False

        # Aplica o flip na imagem base
        if self.virado_esquerda:
             base_image = pygame.transform.flip(self.original_image, True, False)

        # 2. Cálculo e Aplicação da Rotação (Lógica de Correção para Esquerda)
        
        if self.virado_esquerda:
            # Correção: Inverte o Y no atan2 para compensar o flip horizontal,
            # mantendo a verticalidade correta nas diagonais esquerdas.
            # abs(x) garante que o ângulo fique entre -90 e 90.
            angle = -math.degrees(math.atan2(-self.direction.y, abs(self.direction.x) if abs(self.direction.x) > 0.001 else 0.001))
        else:
            # Movimento para a direita (Rotação 360 padrão)
            angle = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        
        self.angle = angle
        
        # 3. Aplicar rotação e centralizar
        self.image = pygame.transform.rotate(base_image, self.angle)
        self.rect = self.image.get_rect(center=center)