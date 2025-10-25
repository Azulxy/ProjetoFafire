import pygame
from camera import Camera
from inimigos import Inimigo
from jogador import Jogador
import config

def jogo_init():
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    pygame.display.set_caption("Crise do Oceano")
    clock = pygame.time.Clock()

    player = Jogador(config.LARGURA_MUNDO // 2, config.ALTURA_MUNDO // 2)
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    todos_sprites.add(player)
    cam = Camera()

    # evento spawn dos inimigos
    SPAWN_EVENTO = pygame.USEREVENT +1
    pygame.time.set_timer(SPAWN_EVENTO, 1000)

    # Fade de início do jogo
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0, 0, 0))
    for alpha in range(255, -1, -10):  # de preto para transparente
        tela.fill((0, 0, 80))
        todos_sprites.draw(tela)
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    rodando = True
    while rodando:
        clock.tick(config.FPS)
        teclas = pygame.key.get_pressed()

        for event in pygame.event.get():
            # Termina o programa se fechar a janela
            if event.type == pygame.QUIT:
                return False
                # Volta pro menu quando aperta ESC
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            elif event.type == SPAWN_EVENTO:
                inimigo_instancia = Inimigo(player)
                todos_sprites.add(inimigo_instancia)
                inimigos.add(inimigo_instancia)

        player.update(teclas)
        inimigos.update()
        cam.atualizar(player)

        # Volta ao menu ao morrer
        if pygame.sprite.spritecollideany(player, inimigos):
            return True

        tela.fill((0, 0, 80))
        for entidade in todos_sprites:
            tela.blit(entidade.image, cam.aplicar(entidade.rect))
        pygame.display.flip()


    # Fade de saída do jogo
    fade = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)
