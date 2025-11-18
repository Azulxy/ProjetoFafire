import pygame
import config

def tela_derrota(tela, tempo_sobrevivido):
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_info = pygame.font.Font(config.CAMINHO_FONTE, 30)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)

    rodando = True

    while rodando:
        tela.fill((120, 20, 20))

        titulo = fonte_titulo.render("VOCÊ FOI DERROTADO!", True, (255, 200, 200))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 120))

        texto_tempo = fonte_info.render(f"Você sobreviveu por {tempo_sobrevivido} segundos!", True, (255, 255, 255))
        tela.blit(texto_tempo, (config.LARGURA_TELA // 2 - texto_tempo.get_width() // 2, 260))

        sub = fonte_sub.render("Pressione ENTER para tentar novamente", True, (255, 255, 255))
        tela.blit(sub, (config.LARGURA_TELA // 2 - sub.get_width() // 2, 400))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"
