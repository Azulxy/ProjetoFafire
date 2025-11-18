import pygame
import random
import config

def mostrar_tela_perk(tela, jogador):
    perks = [
        "Tiro duplo",
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

    mensagem = random.choice(mensagens)

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 36)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 26)
    fonte_perks = pygame.font.Font(config.CAMINHO_FONTE, 28)

    selecionado = 0
    rodando = True

    cor_fundo = (10, 10, 40)
    cor_msg = (255, 255, 255)
    cor_perk_sel = (255, 255, 0)
    cor_perk_normal = (220, 220, 220)

    while rodando:
        tela.fill(cor_fundo)

        # TÍTULO
        titulo = fonte_titulo.render("Escolha um Perk", True, (255, 255, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 60))

        # BALÃO DE FALA
        texto_msg = fonte_msg.render(mensagem, True, cor_msg)

        # Dimensões do balão
        padding = 20
        largura_balao = texto_msg.get_width() + padding * 2
        altura_balao = texto_msg.get_height() + padding * 2
        x_balao = config.LARGURA_TELA // 2 - largura_balao // 2
        y_balao = 140

        # Caixa arredondada
        balao_rect = pygame.Rect(x_balao, y_balao, largura_balao, altura_balao)
        pygame.draw.rect(tela, (30, 30, 70), balao_rect, border_radius=12)
        pygame.draw.rect(tela, (200, 200, 255), balao_rect, 3, border_radius=12)

        # Triângulo do balão
        pygame.draw.polygon(
            tela,
            (30, 30, 70),
            [
                (config.LARGURA_TELA // 2 - 20, y_balao + altura_balao),
                (config.LARGURA_TELA // 2 + 20, y_balao + altura_balao),
                (config.LARGURA_TELA // 2, y_balao + altura_balao + 30)
            ]
        )
        pygame.draw.polygon(
            tela,
            (200, 200, 255),
            [
                (config.LARGURA_TELA // 2 - 20, y_balao + altura_balao),
                (config.LARGURA_TELA // 2 + 20, y_balao + altura_balao),
                (config.LARGURA_TELA // 2, y_balao + altura_balao + 30)
            ],
            3
        )

        # Texto dentro do balão
        tela.blit(texto_msg, (x_balao + padding, y_balao + padding))

        # LISTA DE PERKS
        y_inicio = y_balao + altura_balao + 80

        for i, perk in enumerate(perks):
            cor = cor_perk_sel if i == selecionado else cor_perk_normal
            texto = fonte_perks.render(perk, True, cor)
            x = config.LARGURA_TELA // 2 - texto.get_width() // 2
            y = y_inicio + i * 50
            tela.blit(texto, (x, y))

        pygame.display.flip()

        # CONTROLES
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(perks)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(perks)
                elif evento.key == pygame.K_RETURN:
                    perk_escolhida = perks[selecionado]
                    jogador.aplicar_perk(perk_escolhida)
                    return
