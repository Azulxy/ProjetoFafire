import config
import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=5):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = velocidade
        self.alpha = 255
        self.alpha_sentido = -15 

        # Atributos base
        self.vel_base = 5
        self.vel = self.vel_base
        self.tiros_ativos = 1
        self.vel_tiro = 6
        self.escudo = False
        self.perks_ativos = {}
        self.vida = 3
        self.invencivel = False
        self.tempo_invencivel = 1500
        self.ultimo_hit = 0


    def mover(self, teclas):
        velocidade = self.vel

        # Movimentação
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # Limites do mundo (sem bordas invisíveis extras)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.LARGURA_MUNDO:
            self.rect.right = config.LARGURA_MUNDO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.ALTURA_MUNDO:
            self.rect.bottom = config.ALTURA_MUNDO

    def levar_dano(self, quantidade=1):
        agora = pygame.time.get_ticks()

        if self.invencivel:
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
        else:
            self.image.set_alpha(255)

    def aplicar_perk(self, perk):
        agora = pygame.time.get_ticks()
        duracao = 25000
        self.perks_ativos[perk] = agora + duracao

        # Efeitos das perks
        if perk == "Tiro duplo":
            self.tiros_ativos = 2
        elif perk == "Aumento de velocidade de movimento":
            self.vel = self.vel_base * 1.2
        elif perk == "Tiros mais rápidos":
            self.vel_tiro = 15
        elif perk == "Escudo protetor":
            self.escudo = True

    def atualizar_perks(self):
        agora = pygame.time.get_ticks()
        expirados = [p for p, fim in self.perks_ativos.items() if fim < agora]
        for p in expirados:
            self.remover_perk(p)

    def remover_perk(self, perk):
        if perk in self.perks_ativos:
            del self.perks_ativos[perk]

        # Reverter efeitos
        if perk == "Tiro duplo":
            self.tiros_ativos = 1
        elif perk == "Velocidade +20%":
            self.vel = self.vel_base
        elif perk == "Escudo protetor":
            self.escudo = False
        elif perk == "Tiros mais rápidos":
            self.vel_tiro = 6
        elif perk == "Mais tiros simultâneos":
            self.tiros_ativos = 1
