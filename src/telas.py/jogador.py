import config
import pygame
import math

SCALE_PLAYER = 1.0
JOGADOR_PATH = "assets/imagens/jogador.png"
ESCUDO_PATH = "assets/imagens/escudo.png" # Caminho da imagem do escudo

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=5):
        super().__init__()
        
        # --- CARREGAMENTO DA IMAGEM DO JOGADOR ---
        try:
            self.original_image_loaded = pygame.image.load(JOGADOR_PATH).convert_alpha()
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem em {JOGADOR_PATH}: {e}")
            base_w, base_h = 40, 40
            self.image = pygame.Surface((int(base_w * SCALE_PLAYER), int(base_h * SCALE_PLAYER)), pygame.SRCALPHA).convert_alpha()
            self.image.fill((255, 0, 0))
            
        else:
            original_w, original_h = self.original_image_loaded.get_size()
            w = int(original_w * SCALE_PLAYER)
            h = int(original_h * SCALE_PLAYER)
            self.original_image = pygame.transform.scale(self.original_image_loaded, (w, h))
            self.image = self.original_image
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.posicao_fixa_x = float(self.rect.centerx)
        self.posicao_fixa_y = float(self.rect.centery)

        self.direction = pygame.math.Vector2(1, 0)
        self.virado_esquerda = False

        # --- CARREGAMENTO DA IMAGEM DO ESCUDO ---
        try:
            escudo_original = pygame.image.load(ESCUDO_PATH).convert_alpha()
            # Garante que o escudo tenha o mesmo tamanho (ou ligeiramente maior) que o jogador
            escudo_w = int(self.rect.width * 1.5) # Escala um pouco maior que o jogador
            escudo_h = int(self.rect.height * 1.5)
            self.escudo_image_base = pygame.transform.scale(escudo_original, (escudo_w, escudo_h))
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar a imagem do escudo em {ESCUDO_PATH}: {e}")
            self.escudo_image_base = None

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

    def draw(self, surface, camera_offset=(0, 0)):
            pos_x = self.rect.x - camera_offset[0] # Subtrai
            pos_y = self.rect.y - camera_offset[1] # Subtrai
            surface.blit(self.image, (pos_x, pos_y))

            if self.escudo and self.escudo_image_base:
                # Obtém a posição central do escudo no mundo
                escudo_center_world = (self.posicao_fixa_x, self.posicao_fixa_y)
                
                # Cria um rect centralizado na posição do mundo
                escudo_rect = self.escudo_image_base.get_rect(center=escudo_center_world)
                
                escudo_rect.x -= camera_offset[0]
                escudo_rect.y -= camera_offset[1]
                
                surface.blit(self.escudo_image_base, escudo_rect)

    def mover(self, teclas):
        # ... (Mantido o código de mover) ...
        new_direction = pygame.math.Vector2(0, 0)
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
            new_direction.x = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
            new_direction.x = 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
            new_direction.y = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade
            new_direction.y = 1

        if new_direction.length_squared() > 0:
            self.direction = new_direction.normalize()

        self.posicao_fixa_x = self.rect.centerx
        self.posicao_fixa_y = self.rect.centery

        self.rotacionar()

        # LIMITES DO MUNDO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.LARGURA_MUNDO:
            self.rect.right = config.LARGURA_MUNDO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.ALTURA_MUNDO:
            self.rect.bottom = config.ALTURA_MUNDO

        self.posicao_fixa_x = self.rect.centerx 
        self.posicao_fixa_y = self.rect.centery
    # ROTAÇÃO EM 360 GRAUS (COM FLIP CONDICIONAL PARA MANTER VERTICALIDADE)
    def rotacionar(self):
        center = self.rect.center
        
        base_image = self.original_image
        
        # O componente X determina o flip
        if self.direction.x < 0.0:
            self.virado_esquerda = True
        elif self.direction.x > 0.0:
            self.virado_esquerda = False

        # 1. Flip da imagem base (se necessário)
        if self.virado_esquerda:
             base_image = pygame.transform.flip(self.original_image, True, False)

        # 2. Cálculo e Aplicação da Rotação
        
        if self.virado_esquerda:
            # CORREÇÃO: Invertemos o Y no cálculo do atan2.
            angle = -math.degrees(math.atan2(-self.direction.y, abs(self.direction.x) if abs(self.direction.x) > 0.001 else 0.001))
        else:
            # Movimento para a direita
            angle = -math.degrees(math.atan2(self.direction.y, self.direction.x))
        
        # 3. Aplicar rotação
        self.image = pygame.transform.rotate(base_image, angle)
        self.rect = self.image.get_rect(center=center)
        
        # 4. Mantém o efeito de invencibilidade
        if self.invencivel:
            self.image.set_alpha(self.alpha)
        else:
            self.image.set_alpha(255)

    # DANO + INVENCIBILIDADE ANIMADA
    def levar_dano(self, quantidade=1):
        agora = pygame.time.get_ticks()

        if self.invencivel:
            return

        if self.escudo:
            self.escudo = False
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
        if perk not in self.perks_ativos:
            self.perks_ativos[perk] = 1
        else:
            self.perks_ativos[perk] += 1

        stacks = self.perks_ativos[perk]
        
        # --- Lógica de Aplicação (Mantida) ---
        if perk == "Mais bolhas, menos vel. de bolha":
            self.tiros_ativos = 1 + stacks
            self.vel_tiro = max(3, 6 - (stacks * 0.5)) # Diminui a velocidade do tiro levemente

        elif perk == "Nada mais rápido":
            self.velocidade = self.vel_base * (1 + 0.3 * stacks)

        elif perk == "Mais velocidade de bolha":
            self.vel_tiro = 6 + (1.5 * stacks)

        elif perk == "Escudo protetor":
            agora = pygame.time.get_ticks()
            duracao = 8000 * stacks
            # Armazena o tempo final no dicionário
            self.perks_ativos["Escudo protetor"] = agora + duracao 
            self.escudo = True # Ativa o flag para desenhar

    def atualizar_perks(self):
        agora = pygame.time.get_ticks()

        if "Escudo protetor" in self.perks_ativos:
            tempo_final = self.perks_ativos["Escudo protetor"]
            if isinstance(tempo_final, int) and agora > tempo_final:
                self.escudo = False
                del self.perks_ativos["Escudo protetor"]
        
    def tempo_restante_escudo(self):
        if "Escudo protetor" not in self.perks_ativos:
            return 0

        agora = pygame.time.get_ticks()
        fim = self.perks_ativos["Escudo protetor"]

        restante = (fim - agora) / 1000

        return max(0, restante)

    def remover_perk(self, perk):
        # ... (Lógica de remoção do perk, mantida e ajustada) ...
        if perk in self.perks_ativos:
             if isinstance(self.perks_ativos[perk], int) and perk != "Escudo protetor":
                self.perks_ativos[perk] -= 1
                if self.perks_ativos[perk] <= 0:
                     del self.perks_ativos[perk]
             elif perk == "Escudo protetor":
                  del self.perks_ativos[perk]
                  self.escudo = False # Garante a desativação imediata do escudo
             

        if perk == "Mais bolhas, menos vel. de bolha":
            stacks = self.perks_ativos.get(perk, 0)
            self.tiros_ativos = 1 + stacks
            self.vel_tiro = max(3, 6 - (stacks * 0.5))

        elif perk == "Nada mais rápido":
            stacks = self.perks_ativos.get(perk, 0)
            if stacks == 0:
                self.velocidade = self.vel_base
            else:
                self.velocidade = self.vel_base * (1 + 0.3 * stacks)


        elif perk == "Mais velocidade de bolha":
            stacks = self.perks_ativos.get(perk, 0)
            if stacks == 0:
                 self.vel_tiro = 6
            else:
                 self.vel_tiro = 6 + (1.5 * stacks)

        elif perk == "Escudo protetor":
            self.escudo = False

    def update(self):
        self.atualizar_invencibilidade()
        self.atualizar_perks()