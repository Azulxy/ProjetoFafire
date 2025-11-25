import pygame
import tela_vitoria
import tela_derrota
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

    # --- EVENTO DE SPAWN ---
    SPAWN_EVENTO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENTO, 1200)  # spawn a cada 1.2s

    # --- VARIÁVEIS DE JOGO ---
    inicio_jogo = pygame.time.get_ticks()
    amigo_spawnado = False
    tempo_ultimo_amigo = -1
    ultimo_tiro = 0
    pausado = False

    # --- FADE-IN ---
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0, 0, 0))
    for alpha in range(255, -1, -10):
        config.desenhar_fundo(tela)
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # =========================================================
    # ===================== LOOP DO JOGO ======================
    # =========================================================
    rodando = True
    while rodando:
        clock.tick(config.FPS)
        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()

        # Tempo
        tempo_decorrido = (agora - inicio_jogo) // 1000
        tempo_restante = max(0, 120 - tempo_decorrido)  # 2 minutos

        # ----------- DIFICULDADE (linear) -----------
        # spawn_count aumenta linearmente a cada 30s
        quantidade_spawn = 1 + (tempo_decorrido // 30)
        # velocidade aumenta linearmente: +0.1 a cada 10s (por exemplo)
        vel_inimigo_bonus = (tempo_decorrido // 10) * 0.1

        # =========================================================
        # ========================= EVENTOS ========================
        # =========================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausado = not pausado

                elif event.key == pygame.K_ESCAPE:
                    # ESC apenas sai do jogo a partir da tela jogo
                    return True

            elif event.type == SPAWN_EVENTO and not pausado:
                for _ in range(quantidade_spawn):
                    inimigo_instancia = Inimigo(player, vel_bonus=vel_inimigo_bonus)
                    todos_sprites.add(inimigo_instancia)
                    inimigos.add(inimigo_instancia)

        # =========================================================
        # ==================== SPAWN DO AMIGO ======================
        # =========================================================
        if not amigo_spawnado and not pausado:
            if (tempo_decorrido <= 5 and tempo_ultimo_amigo == -1) or (
                tempo_decorrido > 5
                and tempo_ultimo_amigo != -1
                and agora - tempo_ultimo_amigo >= 30000
            ):
                amigo = Amigo(
                    random.randint(0, config.LARGURA_MUNDO - 40),
                    random.randint(0, config.ALTURA_MUNDO - 40)
                )
                todos_sprites.add(amigo)
                amigos.add(amigo)
                amigo_spawnado = True
                tempo_ultimo_amigo = agora

        # =========================================================
        # ================= COLISÃO COM AMIGO =====================
        # =========================================================
        amigo_encontrado = pygame.sprite.spritecollideany(player, amigos)
        if amigo_encontrado:
            perk = tela_perks.mostrar_tela_perk(tela, player)
            if perk:
                player.aplicar_perk(perk)

            amigo_encontrado.kill()
            amigo_spawnado = False
            tempo_ultimo_amigo = agora

        # =========================================================
        # ==================== ATUALIZAÇÕES ========================
        # =========================================================
        if not pausado:
            player.mover(teclas)
            player.atualizar_perks()        # escudo apenas (permanente os outros perks)
            player.atualizar_invencibilidade()

            # Cor do player (mostra escudo ao coletar)
            if not player.escudo:
                player.image.fill((255, 255, 0))
            else:
                player.image.fill((0, 100, 255))

            inimigos.update()
            tiros.update()
            cam.atualizar(player)

        if tempo_restante == 0:
            resultado = tela_vitoria.tela_vitoria(tela)
            return resultado == "reiniciar"

        # =========================================================
        # ===================== TIROS AUTO =========================
        # =========================================================
        if not pausado and len(inimigos) > 0:
            intervalo_tiro = max(100, int(800 / (player.vel_tiro / 6)))

            if agora - ultimo_tiro > intervalo_tiro:
                inimigos_ordenados = sorted(
                    inimigos,
                    key=lambda i: math.hypot(
                        i.rect.centerx - player.rect.centerx,
                        i.rect.centery - player.rect.centery,
                    )
                )

                for alvo in inimigos_ordenados[: player.tiros_ativos]:
                    tiro = Tiro(
                        player.rect.center,
                        alvo.rect.center,
                        velocidade=player.vel_tiro
                    )
                    todos_sprites.add(tiro)
                    tiros.add(tiro)

                ultimo_tiro = agora

        # Colisão tiros x inimigos
        for tiro in list(tiros):
            if pygame.sprite.spritecollide(tiro, inimigos, True):
                tiro.kill()

        # =========================================================
        # ================== COLISÃO PLAYER ========================
        # =========================================================
        hit = pygame.sprite.spritecollideany(player, inimigos)
        if hit:
            if not player.escudo:
                player.levar_dano()
            else:
                # se tinha escudo, a própria levar_dano já remove escudo; aqui só passa
                pass

            if player.vida <= 0:
                tempo_sobrevivido = (agora - inicio_jogo) // 1000
                resultado = tela_derrota.tela_derrota(tela, tempo_sobrevivido)
                return resultado == "reiniciar"



        # =========================================================
        # ======================= DESENHO ==========================
        # =========================================================
        config.desenhar_fundo(tela, cam.offset.x, cam.offset.y)

        for entidade in todos_sprites:
            tela.blit(entidade.image, cam.aplicar(entidade.rect))

        # =========================================================
        # ======================= HUD ==============================
        # =========================================================
        coracao_cheio = pygame.transform.scale(
            pygame.image.load(config.CAMINHO_CORACAO_CHEIO).convert_alpha(), (32, 32)
        )
        coracao_vazio = pygame.transform.scale(
            pygame.image.load(config.CAMINHO_CORACAO_VAZIO).convert_alpha(), (32, 32)
        )

        x_base = config.LARGURA_TELA - 150
        y_base = 20
        espaco = 45

        for i in range(3):
            if i < player.vida:
                img = coracao_cheio
            else:
                img = coracao_vazio
            tela.blit(img, (x_base + i * espaco, y_base))

        # Tempo
        fonte = pygame.font.Font(config.CAMINHO_FONTE, 28)
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        tela.blit(
            fonte.render(
                f"Sobreviva: {minutos}min {segundos:02d}s", True, config.BRANCO
            ),
            (20, 20)
        )

        # =================== HUD DE STATUS =====================
        status_vel = f"Velocidade: {player.vel:.1f}"
        status_tiros = f"Tiros: {player.tiros_ativos}"
        status_vel_tiro = f"Vel. Tiro: {player.vel_tiro:.1f}"
        status_escudo = f"Escudo: {player.duracao:.1f}" if player.escudo else ""

        tela.blit(fonte.render(status_vel, True, config.BRANCO), (20, 60))
        tela.blit(fonte.render(status_tiros, True, config.BRANCO), (20, 95))
        tela.blit(fonte.render(status_vel_tiro, True, config.BRANCO), (20, 130))

        # Só exibe o escudo se estiver ativo
        if status_escudo:
            tela.blit(fonte.render(status_escudo, True, (0, 170, 255)), (20, 165))

        pygame.display.flip()

    return True