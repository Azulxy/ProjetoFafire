import pygame
import config

def tela_vitoria(tela):
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 28)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)

    mensagem = (
        "Você ajudou o Fred a escapar do lixo e chegar\n"
        "mais perto de encontrar sua família! Cada ação sua\n"
        "mostrou que pequenas atitudes salvam vidas no oceano.\n"
        "Continue protegendo o planeta!"
    )

    rodando = True

    while rodando:
        tela.fill((30, 140, 70))

        # Título
        titulo = fonte_titulo.render("VOCÊ VENCEU!", True, (255, 255, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 80))

        # Mensagem organizada em linhas
        y = 220
        for linha in mensagem.split("\n"):
            render = fonte_msg.render(linha, True, (255, 255, 255))
            tela.blit(render, (config.LARGURA_TELA // 2 - render.get_width() // 2, y))
            y += 40

        # Subtexto
        sub = fonte_sub.render("Pressione ENTER para jogar novamente", True, (255, 255, 255))
        tela.blit(sub, (config.LARGURA_TELA // 2 - sub.get_width() // 2, 450))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"