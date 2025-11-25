import pygame
import random
import math
import config
import os

SPRITE_SHEET_PATH = "assets/imagens/Inimigo_Sprite_Sheet.png"
LINHAS_INIMIGO = 3
COLUNAS_INIMIGO = 5

FRAME_FIXO = None
FRAME_LARGURA = 0
FRAME_ALTURA = 0
SCALE_INIMIGO = 1.0  # escala do sprite (menor que o original)


def carregar_frame_inimigo(corte_topo=0):
    global FRAME_FIXO, FRAME_LARGURA, FRAME_ALTURA

    if FRAME_FIXO is not None:
        return FRAME_FIXO

    sprite = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()

    FRAME_LARGURA = sprite.get_width() // COLUNAS_INIMIGO
    FRAME_ALTURA = sprite.get_height() // LINHAS_INIMIGO

    # --- PEGA SÓ O FRAME 0,0 (primeiro da sheet) ---
    original = pygame.Rect(0, 0, FRAME_LARGURA, FRAME_ALTURA)
    frame = sprite.subsurface(original).copy().convert_alpha()

    # --- APLICAR MESMOS CORTES DO SEU SISTEMA ---
    pixels_corte_topo = int(FRAME_ALTURA * corte_topo)
    corte_esquerda = int(FRAME_LARGURA * 0.15)

    crop_rect = pygame.Rect(
        corte_esquerda,
        pixels_corte_topo,
        FRAME_LARGURA - corte_esquerda,
        FRAME_ALTURA - pixels_corte_topo
    )

    frame = frame.subsurface(crop_rect).copy().convert_alpha()

    # --- ESCALA ---
    nova_w = int(frame.get_width() * SCALE_INIMIGO)
    nova_h = int(frame.get_height() * SCALE_INIMIGO)
    frame = pygame.transform.smoothscale(frame, (nova_w, nova_h))

    FRAME_FIXO = frame
    return FRAME_FIXO


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador, vel_bonus=0):
        super().__init__()

        self.jogador = jogador
        self.frame_base = carregar_frame_inimigo(corte_topo=0.3)

        # frame normal e espelhado
        self.frame_normal = self.frame_base
        self.frame_flip = pygame.transform.flip(self.frame_base, True, False)

        # ESCALA DO INIMIGO (MENOR)
        escala = 0.55
        self.frame_normal = pygame.transform.scale_by(self.frame_normal, escala)
        self.frame_flip = pygame.transform.scale_by(self.frame_flip, escala)

        self.image = self.frame_normal
        self.rect = self.image.get_rect()

        # VELOCIDADE
        self.vel = random.uniform(1.4, 2.2) + vel_bonus

        # POSIÇÃO INICIAL
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

    def update(self):
        # MOVIMENTO EM LINHA RETA EM DIREÇÃO AO PLAYER
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1

        dir_x = dx / dist
        dir_y = dy / dist

        # APLICAR MOVIMENTO
        self.rect.x += dir_x * self.vel
        self.rect.y += dir_y * self.vel

        # VIRAR SPRITE NA DIREÇÃO DO PLAYER
        virar_direita = dx > 0
        old_center = self.rect.center
        self.image = self.frame_flip if virar_direita else self.frame_normal
        self.rect = self.image.get_rect(center=old_center)