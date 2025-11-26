import pygame
import config

# Defina o caminho para o fundo das instruções (ajuste se necessário)
FUNDO_INSTRUCOES_PATH = "assets/imagens/tela_instrucao_fundo.png" 

def tela_instrucoes(tela):
    clock = pygame.time.Clock()

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_texto = pygame.font.Font(config.CAMINHO_FONTE, 30)
    fonte_destaque = pygame.font.Font(config.CAMINHO_FONTE, 32)
    
    # --- Carregar Imagem de Fundo (mantido o seu caminho atualizado) ---
    try:
        fundo_image = pygame.image.load(FUNDO_INSTRUCOES_PATH).convert()
        fundo_image = pygame.transform.scale(fundo_image, (config.LARGURA_TELA, config.ALTURA_TELA))
    except pygame.error:
        print(f"ERRO: Não foi possível carregar o fundo em {FUNDO_INSTRUCOES_PATH}. Usando cor sólida.")
        # Fallback para cor sólida se a imagem não carregar
        fundo_image = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
        fundo_image.fill((5, 10, 50)) 
    # -------------------------------------------------------------------

    # --- Textos Estilizados Fixos ---
    titulo_renderizado = config.cores_textos(
        "INSTRUÇÕES", 
        fonte_titulo, 
        (255, 255, 255), # Branco principal
        (0, 150, 255),   # Azul de borda
        borda=4
    )
    
    instrucao_comecar = config.cores_textos(
        "Pressione QUALQUER TECLA para começar.", 
        fonte_destaque, 
        (255, 200, 0), # Amarelo vibrante
        (255, 50, 50), # Vermelho de borda
        borda=2
    )

    # --- Definição de Estilos ---
    ESTILO_PADRAO = {
        "fonte": fonte_texto,
        "cor1": (200, 230, 255), # Azul claro
        "cor2": (50, 100, 150),  # Azul escuro (borda fina)
        "borda": 1
    }
    
    ESTILO_DESTAQUE = {
        "fonte": fonte_texto,
        "cor1": (255, 255, 0),   # Amarelo puro
        "cor2": (200, 100, 0),   # Laranja/Marrom (borda)
        "borda": 2
    }

    # --- Texto formatado usando os novos estilos ---
    linhas = [
        config.cores_textos("Você é Fred, um peixinho que se perdeu da sua família", **ESTILO_PADRAO),
        config.cores_textos("por causa da poluição deixada pelos humanos.", **ESTILO_PADRAO),
        config.cores_textos("", fonte_texto, config.BRANCO, config.BRANCO, borda=0), # Linha vazia
        
        config.cores_textos("Para sobreviver:", **ESTILO_PADRAO),
        
        # Destaque para comandos
        config.cores_textos(" - Use W A S D ou as setas para se mover", **ESTILO_DESTAQUE),
        config.cores_textos(" - Desvie dos lixos!", **ESTILO_DESTAQUE),
        config.cores_textos(" - Sobreviva por 2 minutos!", **ESTILO_DESTAQUE),
        config.cores_textos("- Peixes amigos podem aparecer e te ajudar.", **ESTILO_DESTAQUE),
        config.cores_textos("Siga a seta amarela para encontrá-los!", **ESTILO_DESTAQUE),

        config.cores_textos("", fonte_texto, config.BRANCO, config.BRANCO, borda=0), # Linha vazia
    ]
    # ----------------------------------------------

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2  # sair
            elif event.type == pygame.KEYDOWN:
                return 0  # iniciar jogo

        # --- DESENHO ---
        tela.blit(fundo_image, (0, 0)) # Desenha o fundo ou a cor de fallback

        # --- TÍTULO ---
        tela.blit(titulo_renderizado, (config.LARGURA_TELA//2 - titulo_renderizado.get_width()//2, 40))

        # TEXTO PRINCIPAL
        # NOTA: y_start foi levemente ajustado para centralizar verticalmente o bloco de texto
        y = config.ALTURA_TELA // 3 - 50 
        espacamento = 38

        for linha_renderizada in linhas:
            # Cálculo de centralização horizontal para cada linha
            x_centralizado = config.LARGURA_TELA // 2 - linha_renderizada.get_width() // 2
            
            tela.blit(linha_renderizada, (x_centralizado, y))
            y += espacamento
            
        # INSTRUÇÃO FINAL (Começar)
        tela.blit(instrucao_comecar, (config.LARGURA_TELA//2 - instrucao_comecar.get_width()//2, config.ALTURA_TELA - 80))


        pygame.display.flip()
        clock.tick(60)

    return 0