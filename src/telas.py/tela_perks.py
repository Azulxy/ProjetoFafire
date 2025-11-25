import pygame
import random
import config
from amigo import AMIGO_PATH
import os

FUNDO_PERK_PATH = "assets/imagens/tela_perk_fundo.png"

def mostrar_tela_perk(tela, jogador):
    # --- Carregamento de Fundo ---
    try:
        fundo_image = pygame.image.load(FUNDO_PERK_PATH).convert()
        fundo_image = pygame.transform.scale(fundo_image, (config.LARGURA_TELA, config.ALTURA_TELA))
    except pygame.error:
        print(f"ERRO: Não foi possível carregar o fundo em {FUNDO_PERK_PATH}. Usando cor sólida.")
        # Fallback (usa a cor sólida original)
        fundo_image = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
        fundo_image.fill((10, 10, 40))

    # --- Carregamento e Preparação do Sprite ---
    try:
        amigo_original = pygame.image.load(AMIGO_PATH).convert_alpha()
        amigo_larg = 140
        amigo_alt = 140
        amigo_image = pygame.transform.scale(amigo_original, (amigo_larg, amigo_alt))
    except pygame.error as e:
        print(f"ERRO ao carregar sprite em tela_perks: {AMIGO_PATH}")
        amigo_larg, amigo_alt = 140, 140
        amigo_image = pygame.Surface((amigo_larg, amigo_alt))
        amigo_image.fill((200, 0, 0))
    # -------------------------------------------
    
    perks = [
        "Mais bolhas, menos vel. de bolha",
        "Nada mais rápido",
        "Mais velocidade de bolha",
        "Escudo protetor"
    ]

    mensagens = [
        "Pequenas atitudes geram grandes mudanças no planeta.",
        "Economize água: cada gota conta!",
        "O lixo que você joga no chão pode ir parar no mar.",
        "Cuidar dos oceanos é cuidar da nossa casa.",
        "Diga não ao plástico descartável. Proteja os oceanos!"
    ]

    perk_escolhida = random.choice(perks)
    mensagem = random.choice(mensagens)

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 36)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 24)
    fonte_opcao = pygame.font.Font(config.CAMINHO_FONTE, 32)
    fonte_perk_nome = pygame.font.Font(config.CAMINHO_FONTE, 32)

    selecionado = 0
    rodando = True

    # --- NOVO POSICIONAMENTO VERTICAL (Elevado) ---
    amigo_x = config.LARGURA_TELA // 2 - amigo_larg // 2
    amigo_y = 230 # Movido de 280 para 180
    amigo_rect = pygame.Rect(amigo_x, amigo_y, amigo_larg, amigo_alt)

    # --- Estilização do Título Fixo ---
    titulo_renderizado = config.cores_textos(
        "Você encontrou um amigo!", 
        fonte_titulo, 
        (255, 255, 100),
        (0, 150, 200),
        borda=3
    )

    # --- Estilização do Rótulo Fixo ---
    rotulo_render = config.cores_textos(
        "Poder encontrado:", 
        fonte_perk_nome,
        (255, 255, 255),
        (0, 150, 200),
        borda=2
    )

    # --- Estilização do Nome do Perk (DESTAQUE) ---
    perk_nome_render = config.cores_textos(
        f"{perk_escolhida}",
        fonte_perk_nome,
        (255, 180, 0),
        (200, 50, 0),
        borda=3
    )
    # -----------------------------------------------------

    while rodando:
        tela.blit(fundo_image, (0, 0))
        
        # ====================== TÍTULO ======================
        tela.blit(titulo_renderizado, (config.LARGURA_TELA // 2 - titulo_renderizado.get_width() // 2, 40))

        # ====================== BALÃO DE FALA ======================
        # O cálculo do balão de fala se ajusta automaticamente ao novo amigo_y
        texto_msg = fonte_msg.render(mensagem, True, (255, 255, 255))
        padding = 25

        largura_balao = texto_msg.get_width() + padding * 2
        altura_balao = texto_msg.get_height() + padding * 2

        x_balao = amigo_x + amigo_larg // 2 - largura_balao // 2
        y_balao = amigo_y - altura_balao - 40

        if x_balao < 20:
            x_balao = 20
        if x_balao + largura_balao > config.LARGURA_TELA - 20:
            x_balao = config.LARGURA_TELA - largura_balao - 20

        if y_balao < 20:
            y_balao = 20

        balao_rect = pygame.Rect(x_balao, y_balao, largura_balao, altura_balao)

        pygame.draw.rect(tela, (30, 30, 70), balao_rect, border_radius=16)
        pygame.draw.rect(tela, (200, 200, 255), balao_rect, 3, border_radius=16)

        centro_amigo = amigo_x + amigo_larg // 2
        triangulo_base_esq = (centro_amigo - 25, y_balao + altura_balao) 
        triangulo_base_dir = (centro_amigo + 25, y_balao + altura_balao)
        triangulo_ponta = (centro_amigo, amigo_y) 

        pygame.draw.polygon(tela, (30, 30, 70),
            [triangulo_ponta, triangulo_base_esq, triangulo_base_dir])
        pygame.draw.polygon(tela, (200, 200, 255),
            [triangulo_ponta, triangulo_base_esq, triangulo_base_dir], 3)

        tela.blit(texto_msg, (x_balao + padding, y_balao + padding))

        # ====================== SPRITE DO AMIGO ======================
        tela.blit(amigo_image, amigo_rect)

        # ====================== INFORMAÇÃO DO PERK ======================
        # A posição y_base é calculada a partir do novo amigo_y
        y_base = amigo_y + amigo_alt + 20 
        
        # 1. RÓTULO DO PERK (Linha 1)
        x_rotulo = config.LARGURA_TELA // 2 - rotulo_render.get_width() // 2
        tela.blit(rotulo_render, (x_rotulo, y_base))

        # 2. NOME DO PERK (Linha 2, com destaque)
        y_perk_nome = y_base + 35
        x_perk_nome = config.LARGURA_TELA // 2 - perk_nome_render.get_width() // 2
        tela.blit(perk_nome_render, (x_perk_nome, y_perk_nome))
        
        # ====================== OPÇÕES ======================
        opcoes = [
            ("Aceitar poder", (100, 255, 100), (0, 150, 0)),
            ("Rejeitar e curar", (255, 100, 100), (150, 0, 0))
        ]

        # Posição inicial das opções (após o nome do perk)
        y_opcoes = y_perk_nome + 50 

        for i, (opc, cor1, cor2) in enumerate(opcoes):
            if i == selecionado:
                render = config.cores_textos(opc, fonte_opcao, (255, 255, 0), (200, 150, 0), borda=3)
            else:
                render = config.cores_textos(opc, fonte_opcao, cor1, cor2, borda=1)
                
            x = config.LARGURA_TELA // 2 - render.get_width() // 2
            tela.blit(render, (x, y_opcoes + i * 50))

        pygame.display.flip()

        # ====================== CONTROLES ======================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % 2

                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % 2

                elif evento.key == pygame.K_RETURN:
                    if selecionado == 0:
                        # Retorna o perk para ser aplicado no jogo_init
                        return perk_escolhida 
                    else:
                        # Aplica a cura imediatamente e retorna None
                        jogador.vida = 3
                        return None