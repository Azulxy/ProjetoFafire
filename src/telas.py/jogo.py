import pygame
import random
import math
import config
from jogador import Jogador
from inimigos import Inimigo
from amigo import Amigo
from tiro import Tiro
from camera import Camera
import tela_perks

def jogo_init():
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    pygame.display.set_caption("Crise dos Oceanos")
    config.FUNDO = config.FUNDO.convert()
    clock = pygame.time.Clock()

    # --- ENTIDADES ---
    player = Jogador(config.LARGURA_MUNDO // 2, config.ALTURA_MUNDO // 2)
    todos_sprites = pygame.sprite.Group(player)
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()
    amigos = pygame.sprite.Group()
    cam = Camera()

    # --- SPAWN EVENTOS ---
    SPAWN_EVENTO = pygame.USEREVENT + 1
    spawn_freq = 1000
    pygame.time.set_timer(SPAWN_EVENTO, spawn_freq)

    inicio_jogo = pygame.time.get_ticks()
    amigo_spawnado = False
    tempo_ultimo_amigo = -1
    ultimo_tiro = 0

    # --- FADE-IN ---
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0,0,0))
    for alpha in range(255, -1, -10):
        config.desenhar_fundo(tela)
        fade.set_alpha(alpha)
        tela.blit(fade, (0,0))
        pygame.display.flip()
        clock.tick(60)

    pausado = False
    rodando = True
    while rodando:
        clock.tick(config.FPS)
        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()
        tempo_decorrido = (agora - inicio_jogo) // 1000
        tempo_restante = max(0, 300 - tempo_decorrido)

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pausado = not pausado
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            elif event.type == SPAWN_EVENTO:
                if not pausado:
                    inimigo_instancia = Inimigo(player)
                    todos_sprites.add(inimigo_instancia)
                    inimigos.add(inimigo_instancia)

        # --- SPAWN AMIGO (1 por vez) ---
        if not amigo_spawnado and not pausado:
            if (tempo_decorrido <= 5 and tempo_ultimo_amigo == -1) or \
               (tempo_decorrido > 5 and tempo_ultimo_amigo != -1 and agora - tempo_ultimo_amigo >= 30000):
                amigo = Amigo(random.randint(0, config.LARGURA_MUNDO - 40),
                              random.randint(0, config.ALTURA_MUNDO - 40))
                todos_sprites.add(amigo)
                amigos.add(amigo)
                amigo_spawnado = True
                tempo_ultimo_amigo = agora

        # --- COLISÕES COM AMIGO ---
        amigo_encontrado = pygame.sprite.spritecollideany(player, amigos)
        if amigo_encontrado:
            perk = tela_perks.mostrar_tela_perk(tela, player)
            if perk:
                player.aplicar_perk(perk)
            amigo_encontrado.kill()
            amigo_spawnado = False
            tempo_ultimo_amigo = agora

        # --- ATUALIZAÇÕES ---
        if not pausado:
            player.mover(teclas)
            player.atualizar_perks()
            inimigos.update()
            tiros.update()
            cam.atualizar(player)

        # --- TIROS AUTOMÁTICOS ---
        if not pausado:
            intervalo_tiro = max(100, int(800 / (player.vel_tiro / 6)))
            if agora - ultimo_tiro > intervalo_tiro and len(inimigos) > 0:
                inimigos_ordenados = sorted(
                    inimigos, 
                    key=lambda i: math.hypot(i.rect.centerx - player.rect.centerx,
                                            i.rect.centery - player.rect.centery)
                )
                for alvo in inimigos_ordenados[:player.tiros_ativos]:
                    tiro = Tiro(player.rect.center, alvo.rect.center, velocidade=player.vel_tiro)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                ultimo_tiro = agora

        # --- COLISÕES TIROS ---
        for tiro in list(tiros):
            if pygame.sprite.spritecollide(tiro, inimigos, True):
                tiro.kill()
        if pygame.sprite.spritecollideany(player, inimigos):
            print("Você foi derrotado!")
            return True
        if tempo_restante == 0:
            print("Você sobreviveu!")
            return True

        # --- DESENHO ---
        config.desenhar_fundo(tela, cam.offset.x, cam.offset.y)
        for entidade in todos_sprites:
            tela.blit(entidade.image, cam.aplicar(entidade.rect))

        # --- DEBUG: DESENHAR HITBOXES ---
        for inimigo in inimigos:
            # 1. Aplica a transformação da câmera ao rect do inimigo
            rect_camera = cam.aplicar(inimigo.rect)

            # 2. Desenha o retângulo na tela:
            # (Surface, Cor, Rect, Espessura_da_Linha)
            pygame.draw.rect(tela, config.VERMELHO, rect_camera, 2)

        # --- HUD ---
        if not pausado:
            fonte = pygame.font.Font(config.CAMINHO_FONTE, 28)
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            tela.blit(fonte.render(f"Sobreviva: {minutos}min {segundos:02d}s", True, config.BRANCO), (20,20))
            if player.perks_ativos:
                ultimo_perk, fim = list(player.perks_ativos.items())[-1]
                restante_seg = max(0, (fim - pygame.time.get_ticks()) // 1000)
                tela.blit(fonte.render(f"{ultimo_perk}: {restante_seg}s", True, config.VERDE), (20,60))

            pygame.display.flip()

    return True
