import pygame
import random
import config

def mostrar_tela_perk(tela, jogador):
    perks = [
        "Mais tiros, tiros mais lentos",
        "Aumento de velocidade de movimento",
        "Tiros mais rápidos",
        "Escudo protetor"
    ]

    mensagens = [
        "Pequenas atitudes geram grandes mudanças no planeta.",
        "Economize água: cada gota conta!",
        "O lixo que você joga no chão pode ir parar no mar.",
        "Cuidar dos oceanos é cuidar da nossa casa.",
        "Diga não ao plástico descartável. Proteja os oceanos!"
    ]

    # -------------- PERK ALEATÓRIO --------------
    perk_escolhida = random.choice(perks)

    # -------------- FRASE ALEATÓRIA --------------
    mensagem = random.choice(mensagens)

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 36)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 24)
    fonte_opcao = pygame.font.Font(config.CAMINHO_FONTE, 32)

    selecionado = 0  # 0 = Aceitar | 1 = Recusar
    rodando = True

    cor_fundo = (10, 10, 40)
    cor_msg = (255, 255, 255)
    cor_sel = (255, 255, 0)
    cor_normal = (200, 200, 200)

    # ---------------- QUADRADO DO AMIGO (substituir por sprite depois) ----------------
    amigo_larg = 140
    amigo_alt = 140
    amigo_x = config.LARGURA_TELA // 2 - amigo_larg // 2
    amigo_y = 280
    amigo_rect = pygame.Rect(amigo_x, amigo_y, amigo_larg, amigo_alt)

    while rodando:
        tela.fill(cor_fundo)

        # ====================== TÍTULO ======================
        titulo = fonte_titulo.render("Você encontrou um amigo!", True, (255, 255, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 40))

        # ====================== BALÃO DE FALA ======================

        texto_msg = fonte_msg.render(mensagem, True, cor_msg)
        padding = 25

        largura_balao = texto_msg.get_width() + padding * 2
        altura_balao = texto_msg.get_height() + padding * 2

        # posição inicial acima do sprite
        x_balao = amigo_x + amigo_larg // 2 - largura_balao // 2
        y_balao = amigo_y - altura_balao - 40

        # ----- Correções para NUNCA sair da tela -----
        if x_balao < 20:
            x_balao = 20
        if x_balao + largura_balao > config.LARGURA_TELA - 20:
            x_balao = config.LARGURA_TELA - largura_balao - 20

        if y_balao < 20:
            y_balao = 20

        balao_rect = pygame.Rect(x_balao, y_balao, largura_balao, altura_balao)

        # Caixa
        pygame.draw.rect(tela, (30, 30, 70), balao_rect, border_radius=16)
        pygame.draw.rect(tela, (200, 200, 255), balao_rect, 3, border_radius=16)

        # Triângulo apontando para o amigo
        centro_amigo = amigo_x + amigo_larg // 2
        triangulo_top = (centro_amigo, y_balao + altura_balao)
        triangulo_esq = (centro_amigo - 25, y_balao + altura_balao + 32)
        triangulo_dir = (centro_amigo + 25, y_balao + altura_balao + 32)

        pygame.draw.polygon(tela, (30, 30, 70),
            [triangulo_top, triangulo_esq, triangulo_dir])
        pygame.draw.polygon(tela, (200, 200, 255),
            [triangulo_top, triangulo_esq, triangulo_dir], 3)

        tela.blit(texto_msg, (x_balao + padding, y_balao + padding))

        # ====================== SPRITE DO AMIGO (por enquanto quadrado verde) ======================
        pygame.draw.rect(tela, (0, 255, 0), amigo_rect)

        # ====================== OPÇÕES ======================
        opcoes = ["Aceitar perk", "Rejeitar e receber cura"]

        y_base = amigo_y + amigo_alt + 50

        for i, opc in enumerate(opcoes):
            cor = cor_sel if i == selecionado else cor_normal
            texto = fonte_opcao.render(opc, True, cor)
            x = config.LARGURA_TELA // 2 - texto.get_width() // 2
            tela.blit(texto, (x, y_base + i * 50))

        # Nome do perk sendo oferecido
        perk_texto = fonte_opcao.render(f"Perk encontrado: {perk_escolhida}", True, (180, 220, 255))
        tela.blit(perk_texto, (config.LARGURA_TELA // 2 - perk_texto.get_width() // 2, y_base - 50))

        pygame.display.flip()

        # ====================== CONTROLES ======================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % 2

                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % 2

                elif evento.key == pygame.K_RETURN:
                    if selecionado == 0:  
                        jogador.aplicar_perk(perk_escolhida)
                    else:  
                        jogador.vida = jogador.vida_maxima
                    return