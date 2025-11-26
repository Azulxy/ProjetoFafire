import pygame
import config

# Define o caminho da imagem de fundo
CAMINHO_FUNDO = "assets/imagens/tela_vitoria_fundo.png"

def tela_vitoria(tela):
    
    # --- CARREGAR RECURSOS ---
    try:
        fundo_imagem = pygame.image.load(CAMINHO_FUNDO).convert()
        # Escala a imagem para o tamanho da tela, se necessário
        fundo_imagem = pygame.transform.scale(
            fundo_imagem, (config.LARGURA_TELA, config.ALTURA_TELA)
        )
    except pygame.error as e:
        print(f"ERRO: Não foi possível carregar a imagem de fundo em {CAMINHO_FUNDO}: {e}")
        fundo_imagem = None # Usa None para desenhar uma cor simples se falhar

    fonte_titulo = pygame.font.Font(config.CAMINHO_FONTE, 60)
    fonte_msg = pygame.font.Font(config.CAMINHO_FONTE, 28)
    fonte_sub = pygame.font.Font(config.CAMINHO_FONTE, 32)
    
    # --- NOVAS CORES VIBRANTES PARA DESTOAR DO FUNDO ---
    
    # Cores do Título (Amarelo brilhante com borda Vermelha)
    cor_titulo_brilhante = (255, 255, 0)
    borda_titulo_contraste = (255, 50, 50) 
    
    # Cores da Mensagem (Verde Neon com borda Preta forte)
    cor_mensagem_neon = (0, 255, 100)
    borda_mensagem_contraste = (0, 0, 0) # Preto, para máximo contraste
    
    # Cores do Subtexto (Ciano com borda Preta)
    cor_subtexto_ciano = (0, 255, 255)
    borda_subtexto_contraste = (0, 0, 0)

    mensagem = (
        "Você ajudou o Fred a escapar do lixo e chegar\n"
        "mais perto de encontrar sua família! Cada ação sua\n"
        "mostrou que pequenas atitudes salvam vidas no oceano.\n"
        "Continue protegendo o planeta!"
    )

    rodando = True

    while rodando:
        # 1. Desenhar Fundo
        if fundo_imagem:
            tela.blit(fundo_imagem, (0, 0))
        else:
            # Cor de backup se a imagem falhar
            tela.fill((30, 140, 70)) 

        # 2. Título (Estilizado com borda)
        if hasattr(config, 'cores_textos'):
            titulo = config.cores_textos(
                "VOCÊ VENCEU!", 
                fonte_titulo, 
                cor_titulo_brilhante, 
                borda_titulo_contraste, 
                borda=3
            )
        else:
            titulo = fonte_titulo.render("VOCÊ VENCEU!", True, cor_titulo_brilhante)
            
        tela.blit(titulo, (config.LARGURA_TELA // 2 - titulo.get_width() // 2, 80))

        # 3. Mensagem organizada em linhas (Verde Neon)
        y = 220
        for linha in mensagem.split("\n"):
            if hasattr(config, 'cores_textos'):
                render = config.cores_textos(
                    linha, 
                    fonte_msg, 
                    cor_mensagem_neon, 
                    borda_mensagem_contraste, 
                    borda=2 # Borda levemente maior para contraste
                )
            else:
                 render = fonte_msg.render(linha, True, cor_mensagem_neon)
                 
            tela.blit(render, (config.LARGURA_TELA // 2 - render.get_width() // 2, y))
            y += 40

        # 4. Subtexto (Ciano)
        if hasattr(config, 'cores_textos'):
            sub = config.cores_textos(
                "Pressione ENTER para jogar novamente", 
                fonte_sub, 
                cor_subtexto_ciano, 
                borda_subtexto_contraste, 
                borda=2
            )
        else:
            sub = fonte_sub.render("Pressione ENTER para jogar novamente", True, cor_subtexto_ciano)
            
        tela.blit(sub, (config.LARGURA_TELA // 2 - sub.get_width() // 2, 450))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "sair"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return "reiniciar"