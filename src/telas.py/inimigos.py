import pygame
import random
import math
import config

# Variáveis globais (ou definidas em config.py, mas movidas para cá se for o caso)
# Se você tiver estas variáveis em config.py, pode removê-las de lá.
SPRITE_SHEET_PATH = "assets/imagens/Inimigo_Sprite_Sheet.png"
LINHAS_INIMIGO = 3
COLUNAS_INIMIGO = 5

# Variável para armazenar os frames e o sprite sheet, inicialmente None
FRAMES_INIMIGO = None
sprite_inimigo = None
FRAME_LARGURA = 0
FRAME_ALTURA = 0

def carregar_frames_inimigo(scale=1.0):
    global FRAMES_INIMIGO, sprite_inimigo, FRAME_LARGURA, FRAME_ALTURA
    
    # Verifica se os frames já foram carregados
    if FRAMES_INIMIGO is not None:
        return

    try:
        # Carrega o sprite sheet (certifique-se de que pygame.init() foi chamado antes desta linha)
        sprite_inimigo = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar sprite sheet: {e}")
        # Trate o erro, talvez retornando uma surface padrão.
        return

    FRAME_LARGURA = sprite_inimigo.get_width() // COLUNAS_INIMIGO
    FRAME_ALTURA = sprite_inimigo.get_height() // LINHAS_INIMIGO

    frames = []
    for linha in range(LINHAS_INIMIGO):
        for coluna in range(COLUNAS_INIMIGO):
            rect = pygame.Rect(coluna*FRAME_LARGURA, linha*FRAME_ALTURA, FRAME_LARGURA, FRAME_ALTURA)
            frame = sprite_inimigo.subsurface(rect).copy().convert_alpha() 
            
            if scale != 1.0:
                frame = pygame.transform.scale(frame, (int(FRAME_LARGURA*scale), int(FRAME_ALTURA*scale)))
                
            frames.append(frame)
    
    FRAMES_INIMIGO = frames

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogador, scale=1.0):
        super().__init__()
        carregar_frames_inimigo(scale=scale)
        self.jogador = jogador
        self.vel = random.uniform(1.5, 3.0)
        self.vida = 10

        frame_original = FRAMES_INIMIGO[0]

        largura_nova = int(frame_original.get_width() * scale)
        altura_nova = int(frame_original.get_height() * scale)
        self.image = frame_original
        
        # OBTÉM O RECT DA IMAGEM ESCALADA CORRETAMENTE
        rect_visual = self.image.get_rect() 
        
        fator_reducao = 0.6 
        
        nova_largura = int(rect_visual.width * fator_reducao)
        nova_altura = int(rect_visual.height * fator_reducao)
        
        self.rect = pygame.Rect(0, 0, nova_largura, nova_altura)

        spawn_pos = rect_visual.copy()
        
        lado = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        
        if lado == 'cima':
            # Usa spawn_pos.width, que agora reflete o tamanho escalado (correto)
            spawn_pos.x = random.randint(0, config.LARGURA_MUNDO - spawn_pos.width) 
            spawn_pos.y = -spawn_pos.height
        elif lado == 'baixo':
            spawn_pos.x = random.randint(0, config.LARGURA_MUNDO - spawn_pos.width)
            spawn_pos.y = config.ALTURA_MUNDO
        elif lado == 'esquerda':
            spawn_pos.x = -spawn_pos.width
            spawn_pos.y = random.randint(0, config.ALTURA_MUNDO - spawn_pos.height)
        else:
            spawn_pos.x = config.LARGURA_MUNDO
            spawn_pos.y = random.randint(0, config.ALTURA_MUNDO - spawn_pos.height)
            
        self.rect.center = spawn_pos.center

    def update(self):
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.vel
        self.rect.y += dy * self.vel