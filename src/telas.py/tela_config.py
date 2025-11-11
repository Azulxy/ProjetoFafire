import pygame
import config

# Volume inicial da música (0.0 a 1.0)
VOLUME_MUSICA = 0.5

def desenhar_slider(tela, x, y, largura, altura, valor):
    # Fundo do slider
    pygame.draw.rect(tela, (100, 100, 100), (x, y, largura, altura))
    # Barra preenchida
    largura_preenchida = int(largura * valor)
    pygame.draw.rect(tela, (0, 200, 255), (x, y, largura_preenchida, altura))
    # Botão circular
    pygame.draw.circle(tela, (255, 255, 255), (x + largura_preenchida, y + altura // 2), altura // 2 + 4)

def atualizar_volume(valor):
    global VOLUME_MUSICA
    VOLUME_MUSICA = max(0.0, min(1.0, valor))
    pygame.mixer.music.set_volume(VOLUME_MUSICA)

def mostrar_tela_config(tela, frames, indice_frame, clock):
    pygame.display.set_caption("Configurações")

    rodando = True
    tempo = 0
    velocidade_animacao = 0.1

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 64)
    titulo = config.cores_textos("CONFIGURAÇÕES", fonte_titulo, (0, 150, 255), (0, 255, 100), borda=4)

    # Slider de volume
    slider_x = config.LARGURA_TELA // 2 - 150
    slider_y = 250
    slider_largura = 300
    slider_altura = 15
    arrastando = False

    while rodando:
        tempo += clock.get_time() / 1000
        if tempo >= velocidade_animacao:
            indice_frame = (indice_frame + 1) % len(frames)
            tempo = 0

        tela.blit(frames[indice_frame], (0, 0))
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 100))

        # Texto e slider
        texto_volume = pygame.font.Font(config.CAMINHO_FONTE, 32).render("Volume da Música", True, (255, 255, 255))
        tela.blit(texto_volume, (config.LARGURA_TELA // 2 - texto_volume.get_width() // 2, slider_y - 40))
        desenhar_slider(tela, slider_x, slider_y, slider_largura, slider_altura, VOLUME_MUSICA)

        # Instrução
        instrucao = config.cores_textos(
            "PRESSIONE ESC PARA VOLTAR AO MENU",
            pygame.font.Font(config.CAMINHO_FONTE, 32),
            (255, 200, 0), (255, 50, 50), borda=2
        )
        tela.blit(instrucao, (config.LARGURA_TELA // 2 - instrucao.get_width() // 2, 350))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if slider_x <= mx <= slider_x + slider_largura and slider_y - 10 <= my <= slider_y + 30:
                        arrastando = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastando = False

            elif evento.type == pygame.MOUSEMOTION and arrastando:
                mx, _ = pygame.mouse.get_pos()
                novo_valor = (mx - slider_x) / slider_largura
                atualizar_volume(novo_valor)

        pygame.display.flip()
        clock.tick(config.FPS)

