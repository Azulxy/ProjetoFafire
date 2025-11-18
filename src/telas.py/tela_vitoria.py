import pygame
import config

def tela_vitoria(tela):
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 28)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)

    mensagem = (
        "Você mandou muito bem! Continue cuidando do planeta\n"
        "e evitando atitudes que poluem a água e o mar.\n"
        "Cada atitude sua faz muita diferença!"
    )

    rodando = True

    while rodando:
        tela.fill((20, 120, 40))

        titulo = fonte_titulo.render("VOCÊ SOBREVIVEU!", True, (255, 255, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 120))

        y = 250
        for linha in mensagem.split("\n"):
            render = fonte_msg.render(linha, True, (255, 255, 255))
            tela.blit(render, (config.LARGURA_TELA // 2 - render.get_width() // 2, y))
            y += 40

        sub = fonte_sub.render("Pressione ENTER para jogar novamente", True, (255, 255, 255))
        tela.blit(sub, (config.LARGURA_TELA // 2 - sub.get_width() // 2, 420))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"

