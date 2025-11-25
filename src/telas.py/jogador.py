import config
import pygame

SCALE_PLAYER = 0.7  # escala do jogador (reduz tamanho visual e a hitbox)

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=5):
        super().__init__()
        # cria superfície e escala para o tamanho desejado
        base_w, base_h = 40, 40
        w = int(base_w * SCALE_PLAYER)
        h = int(base_h * SCALE_PLAYER)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        # MOVIMENTO
        self.velocidade = velocidade
        self.vel_base = 5
        self.vel = self.vel_base

        # TIRO
        self.tiros_ativos = 1
        self.vel_tiro = 6

        # VIDA
        self.vida = 3
        self.invencivel = False
        self.tempo_invencivel = 1500
        self.ultimo_hit = 0
        self.alpha = 255
        self.alpha_sentido = -15

        # PERKS
        self.escudo = False
        self.perks_ativos = {}

    # MOVIMENTO
    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # LIMITES DO MUNDO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.LARGURA_MUNDO:
            self.rect.right = config.LARGURA_MUNDO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.ALTURA_MUNDO:
            self.rect.bottom = config.ALTURA_MUNDO

    # DANO + INVENCIBILIDADE ANIMADA
    def levar_dano(self, quantidade=1):
        agora = pygame.time.get_ticks()

        if self.invencivel:
            return

        if self.escudo:
            # escudo evita o próximo hit
            self.escudo = False
            # opcional: deixar piscando um pouco ao perder o escudo
            self.invencivel = True
            self.ultimo_hit = agora
            return

        self.vida -= quantidade
        if self.vida < 0:
            self.vida = 0

        self.invencivel = True
        self.ultimo_hit = agora

        self.alpha = 255
        self.alpha_sentido = -15

    def atualizar_invencibilidade(self):
        agora = pygame.time.get_ticks()

        if self.invencivel:
            self.alpha += self.alpha_sentido
            if self.alpha <= 30 or self.alpha >= 255:
                self.alpha_sentido *= -1

            self.image.set_alpha(self.alpha)

            if agora - self.ultimo_hit >= self.tempo_invencivel:
                self.invencivel = False
                self.image.set_alpha(255)
                self.alpha = 255

    # SISTEMA DE PERKS
    def aplicar_perk(self, perk):
        # adiciona stack
        if perk not in self.perks_ativos:
            self.perks_ativos[perk] = 1
        else:
            self.perks_ativos[perk] += 1

        stacks = self.perks_ativos[perk]

        # -------------------------------
        # PERK: TIRO DUPLO (AGORA STACKA)
        # -------------------------------
        if perk == "Tiro duplo":
            # Cada stack: +1 tiro e -1 vel de tiro
            self.tiros_ativos = 1 + stacks  
            self.vel_tiro = max(3, 6 - (stacks - 1))  # diminui, mas não passa de 3

        # -----------------------------------------
        # PERK: AUMENTO DE VELOCIDADE DE MOVIMENTO
        # -----------------------------------------
        elif perk == "Aumento de velocidade de movimento":
            self.vel = self.vel_base * (1 + 0.3 * stacks)

        # -----------------------
        # PERK: TIROS MAIS RÁPIDOS
        # -----------------------
        elif perk == "Tiros mais rápidos":
            self.vel_tiro = 6 + (1.5 * stacks)

        # -----------------------
        # PERK: ESCUDO PROTETOR
        # -----------------------
        elif perk == "Escudo protetor":
            agora = pygame.time.get_ticks()
            duracao = 8000 * stacks  # cada stack = +8s
            self.perks_ativos["Escudo protetor"] = agora + duracao
            self.escudo = True

    def atualizar_perks(self):
        agora = pygame.time.get_ticks()

        if "Escudo protetor" in self.perks_ativos:
            tempo_final = self.perks_ativos["Escudo protetor"]
            if isinstance(tempo_final, int) and agora > tempo_final:
                self.escudo = False
                del self.perks_ativos["Escudo protetor"]

    def remover_perk(self, perk):
        if perk in self.perks_ativos:
            del self.perks_ativos[perk]

        if perk == "Tiro duplo":
            self.tiros_ativos = max(1, self.tiros_ativos - 1)

        elif perk == "Aumento de velocidade de movimento":
            self.vel = self.vel_base

        elif perk == "Tiros mais rápidos":
            self.vel_tiro = 6

        elif perk == "Escudo protetor":
            self.escudo = False