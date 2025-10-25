import pygame
import config

def mostrar_tela_inicial(tela, frames, indice_frame, clock):
    pygame.display.set_caption("Inicial")

    tempo = 0
    velocidade_animacao = 0.1
    rodando = True
    continuar = True

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 64)
    fonte_texto = pygame.font.Font(config.CAMINHO_FONTE, 32)

    titulo = config.cores_textos("CRISE DO OCEANO", fonte_titulo, (0, 150, 255), (0, 255, 100), borda=4)
    frase1 = config.cores_textos("TODO OCEANO COMEÇA COM UMA GOTA.", fonte_texto, (9, 28, 176), (0, 150, 255), borda=1)
    frase2 = config.cores_textos("TODO SONHO COMEÇA COM UM PASSO.", fonte_texto, (9, 28, 176), (0, 150, 255), borda=1)
    instrucao = config.cores_textos("PRESSIONE ENTER PARA COMEÇAR", fonte_texto, (255, 200, 0), (255, 50, 50), borda=2)

    pygame.mixer.music.load(config.CAMINHO_MUSICA)
    pygame.mixer.music.play(-1)

    while rodando:
        tempo += clock.get_time() / 1000

        if tempo >= velocidade_animacao:
            indice_frame = (indice_frame + 1) % len(frames)
            tempo = 0

        tela.blit(frames[indice_frame], (0, 0))
        tela.blit(titulo, (config.LARGURA_TELA//2 - titulo.get_width()//2, 100))
        tela.blit(frase1, (config.LARGURA_TELA//2 - frase1.get_width()//2, 200))
        tela.blit(frase2, (config.LARGURA_TELA//2 - frase2.get_width()//2, 260))
        tela.blit(instrucao, (config.LARGURA_TELA//2 - instrucao.get_width()//2, 350))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                continuar = False

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                rodando = False
                continuar = True

        pygame.display.flip()
        clock.tick(config.FPS)

    return continuar, indice_frame