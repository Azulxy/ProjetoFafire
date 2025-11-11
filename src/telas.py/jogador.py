import config
import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=5):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = velocidade

        # Atributos base
        self.vel_base = 5
        self.vel = self.vel_base
        self.vida = 5
        self.tiros_ativos = 1
        self.vel_tiro = 6
        self.escudo = False
        self.perks_ativos = {}

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

    def aplicar_perk(self, perk):
        agora = pygame.time.get_ticks()
        duracao = 25000
        self.perks_ativos[perk] = agora + duracao

        # Efeitos das perks
        if perk == "Tiro duplo":
            self.tiros_ativos = 2
        elif perk == "Velocidade +20%":
            self.vel = self.vel_base * 1.2
        elif perk == "Regenera 1 de vida por 10s":
            self.vida = min(self.vida + 1, 5)
        elif perk == "Tiros mais rápidos":
            self.vel_tiro = 10
        elif perk == "Escudo protetor":
            self.escudo = True
        elif perk == "Mais tiros simultâneos":
            self.tiros_ativos += 1

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
