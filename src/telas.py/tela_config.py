import pygame
import config

def mostrar_tela_config(tela, frames, indice_frame, clock):
    pygame.display.set_caption("Configurações")

    rodando = True
    tempo = 0
    velocidade_animacao = 0.1

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 64)
    titulo = config.cores_textos("CONFIGURAÇÕES", fonte_titulo, (0, 150, 255), (0, 255, 100), borda=4)

    while rodando:
        tempo += clock.get_time() / 1000
        if tempo >= velocidade_animacao:
            indice_frame = (indice_frame + 1) % len(frames)
            tempo = 0

        tela.blit(frames[indice_frame], (0, 0))
        tela.blit(titulo, (config.LARGURA_TELA//2 - titulo.get_width()//2, 100))

        instrucao = config.cores_textos(
            "PRESSIONE ESC PARA VOLTAR AO MENU",
            pygame.font.Font(config.CAMINHO_FONTE, 32),
            (255, 200, 0), (255, 50, 50), borda=2
        )
        tela.blit(instrucao, (config.LARGURA_TELA//2 - instrucao.get_width()//2, 350))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        pygame.display.flip()
        clock.tick(config.FPS)