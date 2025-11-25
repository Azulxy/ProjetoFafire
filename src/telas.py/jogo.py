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
    tela = config.aplicar_fullscreen()
    pygame.display.set_caption("Crise dos Oceanos")
    config.FUNDO = config.FUNDO.convert()
    clock = pygame.time.Clock()

    # --- ENTIDADES ---
    # Inicializa o Jogador no centro do mundo
    player = Jogador(config.LARGURA_MUNDO // 2, config.ALTURA_MUNDO // 2)
    todos_sprites = pygame.sprite.Group(player)
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()
    amigos = pygame.sprite.Group()
    cam = Camera()

    # =========================================================
    # >> CORREÇÃO: ATUALIZAÇÃO INICIAL DA CÂMERA <<
    # Garante que o offset é calculado antes do desenho inicial (e fade-in)
    cam.atualizar(player)
    # =========================================================

    # --- EVENTO DE SPAWN ---
    SPAWN_EVENTO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENTO, 1500)

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
        # Agora o fundo e o jogador são desenhados usando o offset da câmera já calculado
        config.desenhar_fundo(tela, cam.offset.x, cam.offset.y)
        player.draw(tela, cam.offset) # Desenha o jogador sob o fade
        
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    def desenhar_seta_amigo(tela, player, amigo_alvo, cam):
        if amigo_alvo is None:
            return

        # --- Posições na tela ---
        px, py = cam.aplicar_pos(player.rect.center)
        ax, ay = cam.aplicar_pos(amigo_alvo.rect.center)

        # Vetor até o amigo
        dx = ax - px
        dy = ay - py

        angulo = math.atan2(dy, dx)

        ORBITA = 60
        pos_x = px + ORBITA * math.cos(angulo)
        pos_y = py + ORBITA * math.sin(angulo)

        TAM = 14

        local_ponta = (TAM, 0)
        local_lado1 = (-TAM * 0.6, TAM * 0.5)
        local_lado2 = (-TAM * 0.6, -TAM * 0.5)

        def rot(x, y):
            return (
                pos_x + x * math.cos(angulo) - y * math.sin(angulo),
                pos_y + x * math.sin(angulo) + y * math.cos(angulo),
            )

        ponta = rot(*local_ponta)
        l1 = rot(*local_lado1)
        l2 = rot(*local_lado2)

        pygame.draw.polygon(tela, (255, 255, 0), [ponta, l1, l2])

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
        tempo_restante = max(0, 120 - tempo_decorrido)

        # ----------- DIFICULDADE -----------
        quantidade_spawn = 1 + (tempo_decorrido // 30)
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
                amigo_novo = Amigo(
                    random.randint(0, config.LARGURA_MUNDO - 40),
                    random.randint(0, config.ALTURA_MUNDO - 40)
                )
                todos_sprites.add(amigo_novo)
                amigos.add(amigo_novo)
                amigo_spawnado = True
                tempo_ultimo_amigo = agora

        # =========================================================
        # ================= COLISÃO COM AMIGO =====================
        # =========================================================
        amigo_encontrado = pygame.sprite.spritecollideany(player, amigos)
        if amigo_encontrado:
            pausado = True # Pausa o jogo para mostrar a tela de perks
            perk = tela_perks.mostrar_tela_perk(tela, player)
            pausado = False # Retoma o jogo

            if perk:
                player.aplicar_perk(perk)

            amigo_encontrado.kill()
            amigo_spawnado = False
            tempo_ultimo_amigo = agora
        
        # Obtém o amigo atual no grupo
        amigo_alvo = next(iter(amigos), None)

        # =========================================================
        # ==================== ATUALIZAÇÕES ========================
        # =========================================================
        if not pausado:
            player.mover(teclas)
            player.atualizar_perks()
            player.atualizar_invencibilidade()

            inimigos.update()
            tiros.update()
            
            # --- ATUALIZAÇÃO E ROTAÇÃO DO AMIGO ---
            amigo_alvo = next(iter(amigos), None)
            if amigo_alvo:
                amigo_alvo.update(pygame.math.Vector2(player.rect.center))
            # -------------------------------------

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
            if entidade == player:
                # Usa o método draw customizado que inclui a lógica do escudo
                player.draw(tela, cam.offset)
            else:
                # Para todas as outras entidades (tiros, inimigos, amigos), usa o blit normal
                tela.blit(entidade.image, cam.aplicar(entidade.rect))

        # =========================================================
        # ======================= HUD ==============================
        # =========================================================
        # Recarregar imagens do coração dentro do loop é ineficiente, 
        # mas mantido para consistência com o código original.
        coracao_cheio = pygame.transform.scale(
            pygame.image.load(config.CAMINHO_CORACAO_CHEIO).convert_alpha(), (32, 32)
        )
        coracao_vazio = pygame.transform.scale(
            pygame.image.load(config.CAMINHO_CORACAO_VAZIO).convert_alpha(), (32, 32)
        )

        desenhar_seta_amigo(tela, player, amigo_alvo, cam)

        # --- CORAÇÕES: Mantidos no canto superior direito ---
        x_base_coracao = config.LARGURA_TELA - 150
        y_base_coracao = 20
        espaco_coracao = 45

        for i in range(3):
            if i < player.vida:
                img = coracao_cheio
            else:
                img = coracao_vazio
            tela.blit(img, (x_base_coracao + i * espaco_coracao, y_base_coracao))

        # ---------------------------------------------------------
        # 1. TIMER (TOPO CENTRO) - Removido o texto "Sobreviva:"
        # ---------------------------------------------------------
        fonte = pygame.font.Font(config.CAMINHO_FONTE, 28)
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        
        # O texto agora é SÓ o timer no formato Minutos:Segundos
        texto_timer_formatado = f"{minutos}:{segundos:02d}"
        
        texto_tempo = config.cores_textos(
            texto_timer_formatado,
            fonte,
            (255, 200, 0), # Amarelo vibrante
            (255, 50, 50), # Vermelho de borda
            borda=2
        )
        
        # Posição centralizada no topo
        timer_rect = texto_tempo.get_rect(center=(config.LARGURA_TELA // 2, 25))
        tela.blit(texto_tempo, timer_rect)


        # ---------------------------------------------------------
        # 2. HUD DE STATUS (TOPO ESQUERDO)
        # ---------------------------------------------------------
        x_stat = 20
        y_stat_start = 20 # Posição inicial no canto superior esquerdo (abaixo do topo)

        status_vel = f"Velocidade: {player.velocidade:.1f}"
        status_tiros = f"Bolhas: {player.tiros_ativos}"
        status_vel_tiro = f"Vel. bolhas: {player.vel_tiro:.1f}"
        tempo_esc = player.tempo_restante_escudo()
        status_escudo = f"Escudo: {tempo_esc:.0f}s" if tempo_esc > 0 else ""

        # Estilo para os stats básicos
        estilo_base = {
            "fonte": pygame.font.Font(config.CAMINHO_FONTE, 28),
            "cor1": (0, 255, 255), # Ciano
            "cor2": (0, 150, 255), # Azul
            "borda": 2
        }
        
        # Velocidade
        render_vel = config.cores_textos(status_vel, **estilo_base)
        tela.blit(render_vel, (x_stat, y_stat_start))
        
        # Tiros (Abaixo da Velocidade)
        render_tiros = config.cores_textos(status_tiros, **estilo_base)
        tela.blit(render_tiros, (x_stat, y_stat_start + 40))
        
        # Velocidade do Tiro (Abaixo de Tiros)
        render_vel_tiro = config.cores_textos(status_vel_tiro, **estilo_base)
        tela.blit(render_vel_tiro, (x_stat, y_stat_start + 80))

        # Escudo (Estilo diferente, se ativo - Abaixo da Velocidade do Tiro)
        if status_escudo:
            render_escudo = config.cores_textos(
                status_escudo,
                fonte,
                (100, 255, 100), # Verde
                (0, 150, 0),     # Verde Escuro
                borda=2
            )
            tela.blit(render_escudo, (x_stat, y_stat_start + 130))

        pygame.display.flip()

    return True