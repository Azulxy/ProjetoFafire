import config
import pygame

def tela_perk(tela, clock):
    perks = [
        "Tiro duplo",
        "Velocidade +20%",
        "Regenera 1 de vida por 10s"
    ]
    fonte = pygame.font.Font(config.CAMINHO_FONTE, 24)

    selecionado = 0
    while True:
        tela.fill((0, 0, 50))
        for i, perk in enumerate(perks):
            cor = (255, 255, 0) if i == selecionado else (255, 255, 255)
            texto = fonte.render(perk, True, cor)
            tela.blit(texto, (250, 200 + i * 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(perks)
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(perks)
                elif event.key == pygame.K_RETURN:
                    return perks[selecionado]

        pygame.display.flip()
        clock.tick(30)
