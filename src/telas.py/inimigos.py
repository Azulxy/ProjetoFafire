import pygame
import random
import math
import config

# Variáveis globais (ou definidas em config.py, mas movidas para cá se for o caso)
# Se você tiver estas variáveis em config.py, pode removê-las de lá.
SPRITE_SHEET_PATH = config.resource_path("assets/imagens/Inimigo_Sprite_Sheet.png")
LINHAS_INIMIGO = 3
COLUNAS_INIMIGO = 5

# Variável para armazenar os frames e o sprite sheet, inicialmente None
FRAMES_INIMIGO = None
sprite_inimigo = None
FRAME_LARGURA = 0
FRAME_ALTURA = 0

def carregar_frames_inimigo(corte_topo=0):
    global FRAMES_INIMIGO, sprite_inimigo, FRAME_LARGURA, FRAME_ALTURA
    
    if FRAMES_INIMIGO is not None:
        return

    sprite_inimigo = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()

    FRAME_LARGURA = sprite_inimigo.get_width() // COLUNAS_INIMIGO
    FRAME_ALTURA  = sprite_inimigo.get_height() // LINHAS_INIMIGO

    frames = []

    for linha in range(LINHAS_INIMIGO):
        for coluna in range(COLUNAS_INIMIGO):

            # Frame original do sprite sheet
            original_rect = pygame.Rect(
                coluna * FRAME_LARGURA,
                linha * FRAME_ALTURA,
                FRAME_LARGURA,
                FRAME_ALTURA
            )
            frame = sprite_inimigo.subsurface(original_rect).copy().convert_alpha()

            # CORTA DO TOPO
            pixels_corte_topo = int(FRAME_ALTURA * corte_topo)

            # CORTA 15% DA ESQUERDA
            corte_esquerda = int(FRAME_LARGURA * 0.15)

            cropped_rect = pygame.Rect(
                corte_esquerda,
                pixels_corte_topo,
                FRAME_LARGURA - corte_esquerda,
                FRAME_ALTURA - pixels_corte_topo
            )

            frame = frame.subsurface(cropped_rect).copy().convert_alpha()

            frames.append(frame)

    FRAMES_INIMIGO = frames



class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador, scale=1.0):
        super().__init__()
        carregar_frames_inimigo(corte_topo=0.3)



        self.jogador = jogador
        self.vel = random.uniform(1.5, 3.0)

        # Frame exibido
        self.image = FRAMES_INIMIGO[0]
        self.rect = self.image.get_rect()

        if FRAMES_INIMIGO is not None:
            self._frames = FRAMES_INIMIGO
            self._frames_flipped = [pygame.transform.flip(f, True, False) for f in FRAMES_INIMIGO]
        else:
            self._frames = [self.image]
            self._frames_flipped = [pygame.transform.flip(self.image, True, False)]

        lado = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

        if lado == 'cima':
            self.rect.x = random.randint(0, config.LARGURA_MUNDO - self.rect.width)
            self.rect.y = -self.rect.height
        elif lado == 'baixo':
            self.rect.x = random.randint(0, config.LARGURA_MUNDO - self.rect.width)
            self.rect.y = config.ALTURA_MUNDO
        elif lado == 'esquerda':
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, config.ALTURA_MUNDO - self.rect.height)
        else:
            self.rect.x = config.LARGURA_MUNDO
            self.rect.y = random.randint(0, config.ALTURA_MUNDO - self.rect.height)

    def update(self):
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.vel
        self.rect.y += dy * self.vel

        virar = (self.jogador.rect.centerx > self.rect.centerx)

        idx = getattr(self, "anim_index", 0) % len(self._frames)

        frame = self._frames_flipped[idx] if virar else self._frames[idx]

        old_center = self.rect.center
        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.center = old_center