import pygame
import random
import tela_perks
from tiro import Tiro
from camera import Camera
from amigo import Amigo
from inimigos import Inimigo
from jogador import Jogador
import config


def jogo_init():
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    pygame.display.set_caption("Guardião do Oceano")
    clock = pygame.time.Clock()

    # Fundo
    # fundo = pygame.image.load("assets/fundo_oceano.png").convert()
    # fundo = pygame.transform.scale(fundo, (config.LARGURA_TELA, config.ALTURA_TELA))
    fundo = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fundo.fill((0, 0, 0))  # preto

    # Entidades
    player = Jogador(config.LARGURA_MUNDO // 2, config.ALTURA_MUNDO // 2)
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()
    amigos = pygame.sprite.Group()
    todos_sprites.add(player)
    cam = Camera()

    # Eventos
    SPAWN_EVENTO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENTO, 1000)

    # Controle
    inicio_jogo = pygame.time.get_ticks()
    amigo_spawnado = False
    spawn_frequencia = 1000
    proximo_aumento = pygame.time.get_ticks() + 15000  # dificuldade cresce a cada 15s

    # Fade-in
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0, 0, 0))
    for alpha in range(255, -1, -10):
        tela.blit(fundo, (0, 0))
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    rodando = True
    while rodando:
        clock.tick(config.FPS)
        teclas = pygame.key.get_pressed()
        tempo_decorrido = (pygame.time.get_ticks() - inicio_jogo) // 1000
        tempo_restante = max(0, 300 - tempo_decorrido)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                direcao = 1 if player.direcao == "direita" else -1
                tiro = Tiro(player.rect.centerx, player.rect.centery, direcao)
                todos_sprites.add(tiro)
                tiros.add(tiro)
            elif event.type == SPAWN_EVENTO:
                inimigo_instancia = Inimigo(player)
                todos_sprites.add(inimigo_instancia)
                inimigos.add(inimigo_instancia)

        # Dificuldade progressiva
        if pygame.time.get_ticks() > proximo_aumento and spawn_frequencia > 300:
            spawn_frequencia -= 100
            pygame.time.set_timer(SPAWN_EVENTO, spawn_frequencia)
            proximo_aumento = pygame.time.get_ticks() + 15000

        # Spawn do Amigo
        if tempo_decorrido >= 45 and not amigo_spawnado and random.random() < 0.02:
            amigo = Amigo(random.randint(100, config.LARGURA_MUNDO - 100),
                          random.randint(100, config.ALTURA_MUNDO - 100))
            amigos.add(amigo)
            todos_sprites.add(amigo)
            amigo_spawnado = True

        # Atualizações
        player.update(teclas)
        inimigos.update()
        tiros.update()
        cam.atualizar(player)

        # Colisões
        for tiro in tiros:
            if pygame.sprite.spritecollide(tiro, inimigos, True):
                tiro.kill()

        # Player colide com inimigo → derrota
        if pygame.sprite.spritecollideany(player, inimigos):
            print("Você foi derrotado!")
            rodando = False

        # Player encontra o amigo → abre tela de perk com diálogo educativo
        amigo_encontrado = pygame.sprite.spritecollideany(player, amigos)
        if amigo_encontrado:
            mensagem_educativa = random.choice([
                "Os corais estão morrendo devido ao aquecimento global!",
                "Plásticos no oceano matam milhares de animais todos os anos!",
                "Preservar o mar é preservar a vida na Terra!"
            ])
            perk = tela_perks.tela_perk(tela, clock, mensagem_educativa)
            print("Perk escolhida:", perk)
            amigo_encontrado.kill()

        # Vitória
        if tempo_restante == 0:
            print("Você sobreviveu! 🌊")
            rodando = False

        # Desenho na tela
        tela.blit(fundo, (0, 0))
        for entidade in todos_sprites:
            tela.blit(entidade.image, cam.aplicar(entidade.rect))

        # HUD
        fonte = pygame.font.Font(config.CAMINHO_FONTE, 28)
        texto_tempo = fonte.render(f"Sobreviva: {tempo_restante}s", True, (255, 255, 255))
        tela.blit(texto_tempo, (20, 20))

        pygame.display.flip()

    # Fade-out
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)
