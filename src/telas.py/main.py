import pygame
import config
import tela_inicial
import tela_menu
import tela_config

def main():
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    frames = config.carregar_frames()

    indice_frame = 0
    clock = config.CLOCK
    rodando = True

    while rodando:
        continuar, indice_frame = tela_inicial.mostrar_tela_inicial(tela, frames, indice_frame, clock)
        if not continuar:
            break

        while True:
            indice_menu, indice_frame = tela_menu.mostrar_tela_menu(tela, frames, indice_frame, clock)

            if indice_menu == 0:  # Jogar
                print("Iniciando o jogo...")  
                continue

            elif indice_menu == 1:  # Configurações
                tela_config.mostrar_tela_config(tela, frames, indice_frame, clock)
                continue

            elif indice_menu == 2:  # Sair
                rodando = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()