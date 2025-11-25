import pygame
import config

def tela_derrota(tela, tempo_sobrevivido):
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 30)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)

    mensagem = (
        "Oh não! Fred acabou se perdendo em meio ao lixo do oceano.\n"
        "Mas cada nova tentativa deixa ele mais perto de reencontrar\n"
        "sua família. Vamos tentar ajudar o Fred mais uma vez?"
    )

    rodando = True

    while rodando:
        tela.fill((150, 40, 40))

        # Título grande
        titulo = fonte_titulo.render("VOCÊ FOI DERROTADO!", True, (255, 220, 220))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 80))

        # Caixa central para a mensagem
        linhas = mensagem.split("\n")
        y = 200
        for linha in linhas:
            render = fonte_msg.render(linha, True, (255, 255, 255))
            tela.blit(render, (config.LARGURA_TELA // 2 - render.get_width() // 2, y))
            y += 40

        # Tempo sobrevivido
        texto_tempo = fonte_msg.render(
            f"Você protegeu o Fred por {tempo_sobrevivido} segundos!",
            True,
            (255, 255, 180)
        )
        tela.blit(texto_tempo, (
            config.LARGURA_TELA // 2 - texto_tempo.get_width() // 2,
            y + 30
        ))

        # Subtexto
        sub = fonte_sub.render("Pressione ENTER para tentar novamente", True, (255, 255, 255))
        tela.blit(sub, (config.LARGURA_TELA // 2 - sub.get_width() // 2, 450))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"