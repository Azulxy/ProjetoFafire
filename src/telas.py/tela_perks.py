import pygame
import random
import config

def mostrar_tela_perk(tela, jogador):
    perks = [
        "Tiro duplo",
        "Velocidade +20%",
        "Regenera 1 de vida por 10s",
        "Tiros mais rápidos",
        "Escudo protetor",
        "Mais tiros simultâneos"
    ]

    mensagens = [
        "Pequenas atitudes geram grandes mudanças no planeta.",
        "Economize água: cada gota conta!",
        "O lixo que você joga no chão pode ir parar no mar.",
        "Cuidar dos oceanos é cuidar da nossa casa.",
        "Diga não ao plástico descartável. Proteja os oceanos!"
    ]

    mensagem = random.choice(mensagens)

    fonte = pygame.font.Font(config.CAMINHO_FONTE, 28)
    fonte_menor = pygame.font.Font(config.CAMINHO_FONTE, 22)
    selecionado = 0
    rodando = True

    while rodando:
        tela.fill((10, 10, 40))

        # Título
        titulo = fonte.render("Escolha um Perk", True, (255, 255, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 100))

        # Lista de perks
        for i, perk in enumerate(perks):
            cor = (0, 255, 0) if i == selecionado else (255, 255, 255)
            texto = fonte.render(perk, True, cor)
            tela.blit(texto, (config.LARGURA_TELA // 2 - texto.get_width() // 2, 200 + i * 50))

        # Mensagem ambiental aleatória
        texto_msg = fonte_menor.render(mensagem, True, (100, 255, 100))
        tela.blit(texto_msg, (config.LARGURA_TELA // 2 - texto_msg.get_width() // 2, config.ALTURA_TELA - 100))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(perks)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(perks)
                elif evento.key == pygame.K_RETURN:
                    perk_escolhido = perks[selecionado]
                    jogador.aplicar_perk(perk_escolhido)
                    return
