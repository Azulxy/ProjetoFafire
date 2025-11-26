import pygame
import config
import math

# Volume inicial da música (0.0 a 1.0)
VOLUME_MUSICA = 0.5

# Intervalo de tempo mínimo entre pressionamentos de tecla para navegação/alteração
INTERVALO_TECLA = 150 

# --- FUNÇÕES DE UTENSÍLIOS ---

def desenhar_slider(tela, x, y, largura, altura, valor, cor_foco=(255, 255, 255)):
    # Cores de Estilização
    cor_fundo = (50, 50, 50)  # Cinza escuro
    cor_cheio = (0, 200, 255) # Ciano/Azul claro
    cor_knob = (255, 255, 0)  # Amarelo

    # 1. Fundo do Slider
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura), border_radius=4)
    
    # 2. Preenchimento (Valor Atual)
    largura_preenchida = int(largura * valor)
    pygame.draw.rect(tela, cor_cheio, (x, y, largura_preenchida, altura), border_radius=4)
    
    # 3. Knob (Círculo Arrastável)
    # Se estiver focado, desenha uma borda extra ao redor
    if cor_foco != (255, 255, 255):
        pygame.draw.circle(
            tela, cor_foco,
            (x + largura_preenchida, y + altura // 2),
            altura // 2 + 6
        )

    pygame.draw.circle(
        tela, cor_knob,
        (x + largura_preenchida, y + altura // 2),
        altura // 2 + 4
    )


def atualizar_volume(valor):
    global VOLUME_MUSICA
    VOLUME_MUSICA = max(0.0, min(1.0, valor))
    pygame.mixer.music.set_volume(VOLUME_MUSICA)

# --- FUNÇÃO DE APLICAÇÃO DE FULLSCREEN ---

def toggle_fullscreen():
    config.FULLSCREEN_ATIVADO = not config.FULLSCREEN_ATIVADO
    return config.aplicar_fullscreen()


# --- FUNÇÃO PRINCIPAL ---

def mostrar_tela_config(tela, frames, indice_frame, clock):
    pygame.display.set_caption("Configurações")

    rodando = True
    tempo = 0
    velocidade_animacao = 0.1

    # Estilo dos Textos
    cor_titulo = (0, 150, 255)
    borda_titulo = (0, 255, 100)
    cor_botoes = (255, 255, 0)
    borda_botoes = (200, 0, 0)
    
    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 64)
    titulo = config.cores_textos(
        "CONFIGURAÇÕES", fonte_titulo,
        cor_titulo, borda_titulo, borda=4
    )

    # 1. Slider de Volume
    slider_x = config.LARGURA_TELA // 2 - 150
    slider_y = 250
    slider_largura = 300
    slider_altura = 15
    arrastando = False

    # 2. Botão FULLSCREEN
    fonte_botao = pygame.font.Font(config.CAMINHO_FONTE, 32)
    botao_y = 380 
    texto_botao = lambda: (
        "FULLSCREEN: ON" if config.FULLSCREEN_ATIVADO else "FULLSCREEN: OFF"
    )

    # --- Variáveis de Navegação por Teclado ---
    foco_elemento = 0 # 0: Slider Volume, 1: Botão Fullscreen
    elementos_focaveis = 2
    ultimo_pressionamento_tecla = 0


    while rodando:
        agora = pygame.time.get_ticks()
        clock.tick(config.FPS)
        
        # Animação de fundo
        tempo += clock.get_time() / 1000
        if tempo >= velocidade_animacao:
            indice_frame = (indice_frame + 1) % len(frames)
            tempo = 0

        # --- SEÇÃO DE DESENHO PRINCIPAL ---
        tela.blit(frames[indice_frame], (0, 0))
        
        # Título
        tela.blit(titulo, (
            config.LARGURA_TELA // 2 - titulo.get_width() // 2,
            100
        ))

        # --- SLIDER DE VOLUME ---
        
        # Cor de foco (Amarelo)
        cor_slider_foco = (255, 255, 0) if foco_elemento == 0 else (255, 255, 255)
        
        # Texto Volume estilizado
        texto_volume = config.cores_textos(
            "VOLUME DA MÚSICA", 
            pygame.font.Font(config.CAMINHO_FONTE, 32),
            (255, 255, 255), cor_slider_foco, borda=2
        )
        tela.blit(
            texto_volume,
            (config.LARGURA_TELA // 2 - texto_volume.get_width() // 2,
             slider_y - 40)
        )

        # Desenhar Slider
        desenhar_slider(
            tela, slider_x, slider_y,
            slider_largura, slider_altura,
            VOLUME_MUSICA,
            cor_foco=cor_slider_foco # Passa a cor de foco para a função
        )

        # --- BOTÃO FULLSCREEN ---
        
        cor_botao_borda = (0, 255, 0) if foco_elemento == 1 else (200, 0, 0)
        cor_texto_botao = (255, 255, 0) 

        # Renderiza o texto do botão com o estilo cores_textos
        botao_render = config.cores_textos(
            texto_botao(), fonte_botao,
            cor_texto_botao, cor_botao_borda, borda=3
        )
        # Centraliza o retângulo do botão
        botao_rect = botao_render.get_rect(center=(config.LARGURA_TELA // 2, botao_y))
        
        # Desenha o texto estilizado
        tela.blit(botao_render, botao_rect)

        # Instrução ESC
        instrucao = config.cores_textos(
            "PRESSIONE ESC PARA VOLTAR AO MENU",
            pygame.font.Font(config.CAMINHO_FONTE, 32),
            (255, 200, 0), (255, 50, 50), borda=2
        )
        tela.blit(
            instrucao,
            (config.LARGURA_TELA // 2 - instrucao.get_width() // 2, 520)
        )
        # -----------------------------------

        # EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                
                # --- Navegação e Ação (W, S, A, D, ENTER) ---
                elif agora - ultimo_pressionamento_tecla > INTERVALO_TECLA:
                    
                    # 1. Navegação Vertical (W, S)
                    if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                        foco_elemento = (foco_elemento + 1) % elementos_focaveis
                        ultimo_pressionamento_tecla = agora
                    elif evento.key == pygame.K_w or evento.key == pygame.K_UP:
                        foco_elemento = (foco_elemento - 1 + elementos_focaveis) % elementos_focaveis
                        ultimo_pressionamento_tecla = agora

                    # 2. Ações do Elemento Focado
                    
                    # 2.1. SLIDER (Foco 0): Ajuste A/D
                    elif foco_elemento == 0:
                        if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                            novo_valor = VOLUME_MUSICA - 0.05
                            atualizar_volume(novo_valor)
                            ultimo_pressionamento_tecla = agora
                        elif evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                            novo_valor = VOLUME_MUSICA + 0.05
                            atualizar_volume(novo_valor)
                            ultimo_pressionamento_tecla = agora

                    # 2.2. BOTÃO FULLSCREEN (Foco 1): Ação ENTER
                    elif foco_elemento == 1:
                        if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                            tela = toggle_fullscreen()
                            
                            # Força o redesenho imediato após fullscreen
                            tela.blit(frames[indice_frame], (0, 0))  
                            pygame.display.flip()  
                            ultimo_pressionamento_tecla = agora

            # --- Eventos de Mouse ---
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Slider: Clique
                if slider_x <= mx <= slider_x + slider_largura and slider_y - 10 <= my <= slider_y + 30:
                    arrastando = True
                    foco_elemento = 0 # Define foco no Slider ao clicar

                # Botão FULLSCREEN: Clique
                if botao_rect.collidepoint(mx, my):
                    foco_elemento = 1 # Define foco no Botão ao clicar
                    tela = toggle_fullscreen()
                    
                    # Força o redesenho imediato após fullscreen
                    tela.blit(frames[indice_frame], (0, 0))  
                    pygame.display.flip()  

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastando = False

            elif evento.type == pygame.MOUSEMOTION and arrastando:
                mx, _ = pygame.mouse.get_pos()
                novo_valor = (mx - slider_x) / slider_largura
                atualizar_volume(novo_valor)

        # Flip principal (para o próximo frame)
        pygame.display.flip()