import pygame
import config
import os

# Defina o caminho para o fundo da tela de derrota
FUNDO_DERROTA_PATH = "assets/imagens/tela_derrota_fundo.png"

def tela_derrota(tela, tempo_sobrevivido):
    
    # --- Carregar Imagem de Fundo ---
    try:
        fundo_image = pygame.image.load(FUNDO_DERROTA_PATH).convert()
        fundo_image = pygame.transform.scale(fundo_image, (config.LARGURA_TELA, config.ALTURA_TELA))
    except pygame.error:
        print(f"ERRO: Não foi possível carregar o fundo em {FUNDO_DERROTA_PATH}. Usando cor de fallback.")
        # Fallback para cor sólida (tom de poluição/derrota)
        fundo_image = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
        fundo_image.fill((80, 20, 20)) # Vermelho escuro/marrom
    # --------------------------------

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 30)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)
    
    # --- Estilização dos Textos ---
    
    # Título (VERMELHO DE DERROTA)
    titulo_renderizado = config.cores_textos(
        "VOCÊ FOI DERROTADO!", 
        fonte_titulo, 
        (255, 100, 100),   # Vermelho claro principal
        (150, 0, 0),       # Vermelho escuro/borda
        borda=5
    )
    
    # Mensagem Central (AZUL TRISTE)
    mensagem = (
        "Oh não! Fred acabou se perdendo em meio ao lixo do oceano.",
        "Mas cada nova tentativa deixa ele mais perto de reencontrar",
        "sua família. Vamos tentar ajudar o Fred mais uma vez?"
    )
    
    # Tempo Sobrevivido (AMARELO DE DESTAQUE)
    texto_tempo_render = config.cores_textos(
        f"Você protegeu o Fred por {tempo_sobrevivido} segundos!",
        fonte_msg,
        (255, 255, 100),   # Amarelo
        (180, 180, 0),     # Amarelo escuro/borda
        borda=2
    )
    
    # Subtexto/Instrução (VERDE/AMARELO DE AÇÃO)
    sub_render = config.cores_textos(
        "Pressione ENTER para tentar novamente",
        fonte_sub,
        (100, 255, 100),   # Verde claro
        (0, 150, 0),       # Verde escuro/borda
        borda=3
    )

    rodando = True

    while rodando:
        
        # Desenha o fundo (imagem ou fallback)
        tela.blit(fundo_image, (0, 0))

        # Título grande
        tela.blit(titulo_renderizado, (config.LARGURA_TELA // 2 - titulo_renderizado.get_width() // 2, 80))

        # Caixa central para a mensagem
        y = 200
        espacamento = 40
        
        for linha_texto in mensagem:
            # Renderiza cada linha com um estilo padrão para texto longo
            render = config.cores_textos(
                linha_texto, 
                fonte_msg, 
                (200, 200, 255),  # Azul pálido
                (50, 50, 100),    # Borda azul escura
                borda=1
            )
            
            tela.blit(render, (config.LARGURA_TELA // 2 - render.get_width() // 2, y))
            y += espacamento

        # Tempo sobrevivido
        tela.blit(texto_tempo_render, (
            config.LARGURA_TELA // 2 - texto_tempo_render.get_width() // 2,
            y + 30
        ))

        # Subtexto
        tela.blit(sub_render, (config.LARGURA_TELA // 2 - sub_render.get_width() // 2, 450))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"