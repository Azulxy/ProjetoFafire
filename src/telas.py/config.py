import os
import pygame

# CONFIGURAÇÃO DE TELA
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
CINZA = (128, 128, 128)
AMARELO = (255, 255, 0)

# PATHS
CAMINHO_FUNDO = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'imagens', 'background.jpg')
CAMINHO_FRAMES = "assets/frames"
CAMINHO_FONTE = "assets/fontes/fonte_pixel.ttf"
CAMINHO_MUSICA = "assets/sons/musica_intro.mp3"

# FUNDO
FUNDO = pygame.image.load(CAMINHO_FUNDO)
ESCALA_FUNDO = 0.8
largura_original, altura_original = FUNDO.get_size()
LARGURA_MUNDO = int(largura_original * ESCALA_FUNDO)
ALTURA_MUNDO = int(altura_original * ESCALA_FUNDO)
FUNDO = pygame.transform.scale(FUNDO, (LARGURA_MUNDO, ALTURA_MUNDO))

CLOCK = pygame.time.Clock()

# Carrega frames de fundo (opcional)
def carregar_frames():
    frames = []
    if os.path.exists(CAMINHO_FRAMES):
        lista_frames = sorted(os.listdir(CAMINHO_FRAMES))
        for f in lista_frames:
            caminho_frame = os.path.join(CAMINHO_FRAMES, f)
            try:
                frame = pygame.image.load(caminho_frame).convert_alpha()
                frame = pygame.transform.scale(frame, (LARGURA_TELA, ALTURA_TELA))
                frames.append(frame)
            except pygame.error as e:
                print(f"Erro ao carregar frame {f}: {e}")
    else:
        print("Pasta de frames não encontrada!")
        frame = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        frame.fill((0, 0, 0))
        frames = [frame]
    return frames

# DESENHAR FUNDO
def desenhar_fundo(tela, camera_x=0, camera_y=0):
    tela.blit(FUNDO, (-camera_x, -camera_y))

# FUNÇÃO DE TEXTO COM GRADIENTE E BORDA
def cores_textos(texto, fonte, cor1, cor2, borda=3):
    texto_surface = fonte.render(texto, True, (255, 255, 255))
    largura, altura = texto_surface.get_size()

    gradiente = pygame.Surface((largura, altura)).convert_alpha()
    for y in range(altura):
        r = cor1[0] + (cor2[0] - cor1[0]) * y // altura
        g = cor1[1] + (cor2[1] - cor1[1]) * y // altura
        b = cor1[2] + (cor2[2] - cor1[2]) * y // altura
        pygame.draw.line(gradiente, (r, g, b), (0, y), (largura, y))

    gradiente.blit(texto_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    borda_surface = pygame.Surface((largura + borda*2, altura + borda*2), pygame.SRCALPHA)
    for dx in range(-borda, borda+1):
        for dy in range(-borda, borda+1):
            if dx != 0 or dy != 0:
                borda_surface.blit(fonte.render(texto, True, (0, 0, 0)), (dx+borda, dy+borda))
    
    borda_surface.blit(gradiente, (borda, borda))
    return borda_surface
