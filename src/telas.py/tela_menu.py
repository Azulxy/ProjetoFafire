import pygame
import config

def mostrar_tela_menu(tela, frames, indice_frame, clock):
    pygame.display.set_caption("Menu")

    rodando = True
    tempo = 0
    velocidade_animacao = 0.1

    # Fonte
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 64)
    fonte_opcao = pygame.font.Font(config.CAMINHO_FONTE, 40)

    # Textos
    titulo = config.cores_textos("MENU PRINCIPAL", fonte_titulo, (0, 150, 255), (0, 255, 100), borda=4)
    opcoes_texto = ["JOGAR", "CONFIGURAÇÕES", "SAIR"]

    indice = 0

    while rodando:
        tempo += clock.get_time() / 1000
        if tempo >= velocidade_animacao:
            indice_frame = (indice_frame + 1) % len(frames)
            tempo = 0

        tela.blit(frames[indice_frame], (0, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 100))

        # Gradiente
        for i, texto in enumerate(opcoes_texto):
            if i == indice:
                render_opcao = config.cores_textos(texto, fonte_opcao, (255, 255, 0), (255, 100, 0), borda=2)

            else:
                if texto == "JOGAR":
                    render_opcao = config.cores_textos(texto, fonte_opcao, (255, 200, 0), (255, 50, 50), borda=2)

                elif texto == "CONFIGURAÇÕES":
                    render_opcao = config.cores_textos(texto, fonte_opcao, (0, 255, 255), (0, 100, 200), borda=2)

                elif texto == "SAIR":
                    render_opcao = config.cores_textos(texto, fonte_opcao, (255, 0, 0), (150, 0, 0), borda=2)
                    
            tela.blit(render_opcao, (config.LARGURA_TELA // 2 - render_opcao.get_width() // 2, 250 + i*80))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                indice = 2

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    indice = (indice + 1) % len(opcoes_texto)

                elif evento.key == pygame.K_UP:
                    indice = (indice - 1) % len(opcoes_texto)

                elif evento.key == pygame.K_RETURN:
                    rodando = False

                elif evento.key == pygame.K_ESCAPE:
                    rodando = False
                    indice = 2

        pygame.display.flip()
        clock.tick(config.FPS)

    return indice, indice_frame