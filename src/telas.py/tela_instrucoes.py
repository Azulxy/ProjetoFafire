import pygame
import config

def tela_instrucoes(tela):
    clock = pygame.time.Clock()

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_texto = pygame.font.Font(config.CAMINHO_FONTE, 30)

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2  # sair
            elif event.type == pygame.KEYDOWN:
                return 0  # iniciar jogo

        tela.fill((5, 10, 50))

        # --- TÍTULO ---
        titulo = fonte_titulo.render("INSTRUÇÕES", True, config.BRANCO)
        tela.blit(titulo, (config.LARGURA_TELA//2 - titulo.get_width()//2, 40))

        # TEXTO PRINCIPAL
        botoom_margin = 120
        x = 60
        y = 150
        espacamento = 38

        linhas = [
            "Você é Fred, um peixinho que se perdeu da sua família",
            "por causa da poluição deixada pelos humanos.",
            "",
            "Para sobreviver:",
            " - Use W A S D ou as setas para se mover",
            " - Desvie dos lixos!",
            "",
            "Peixes amigos podem aparecer e te ajudar com",
            "habilidades especiais. Fique atento!",
            "",
            "Pressione qualquer tecla para começar.",
        ]

        for linha in linhas:
            texto = fonte_texto.render(linha, True, config.BRANCO)
            tela.blit(texto, (x, y))
            y += espacamento

        pygame.display.flip()
        clock.tick(60)

    return 0