import pygame
import jogo
import config
import tela_inicial
import tela_menu
import tela_config

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    pygame.display.set_caption("Crise dos Oceanos")
    frames = config.carregar_frames()
    indice_frame = 0
    clock = config.CLOCK
    rodando = True

    while rodando:
        # --- Tela inicial ---
        continuar, indice_frame = tela_inicial.mostrar_tela_inicial(tela, frames, indice_frame, clock)

        if not continuar:
            break

        # --- Menu ---
        menu_ativo = True

        while menu_ativo:
            indice_menu, indice_frame = tela_menu.mostrar_tela_menu(tela, frames, indice_frame, clock)

            if indice_menu == 0:  # Jogar
                voltar_menu = jogo.jogo_init()
                menu_ativo = False

                if not voltar_menu:
                    rodando = False

            elif indice_menu == 1:  # Configurações
                tela_config.mostrar_tela_config(tela, frames, indice_frame, clock)

            elif indice_menu == 2:  # Sair
                rodando = False
                menu_ativo = False

    pygame.quit()

if __name__ == "__main__":
    main()