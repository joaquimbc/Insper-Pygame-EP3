import sys
import pygame
from random import randint

# Constantes do jogo
LARGURA, ALTURA = 800, 600
RAIO_BOLA = 10
LARGURA_RAQUETE, ALTURA_RAQUETE = 15, 80
FPS = 60
TAMANHO_FONTE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self, win, clock, font):
        self.win = win
        self.clock = clock
        self.font = font
        self.bola_dx, self.bola_dy = 3, 3
        self.raquete_velocidade = 4
        self.score1, self.score2 = 0, 0
        self.bola_x, self.bola_y = LARGURA // 2, ALTURA // 2
        self.raquete1_y, self.raquete2_y = ALTURA // 2, ALTURA // 2
        self.player1 = Player("Player 1", 'vertical')
        self.player2 = Player("Player 2", 'vertical')

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.movimenta_raquete()
            self.movimenta_bola()
            self.renderiza_jogo()
            self.clock.tick(FPS)

    def movimenta_raquete(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.raquete1_y - self.raquete_velocidade > 0:
            self.raquete1_y -= self.raquete_velocidade
        if keys[pygame.K_s] and self.raquete1_y + self.raquete_velocidade < ALTURA - ALTURA_RAQUETE:
            self.raquete1_y += self.raquete_velocidade

        if keys[pygame.K_UP] and self.raquete2_y - self.raquete_velocidade > 0:
            self.raquete2_y -= self.raquete_velocidade
        if keys[pygame.K_DOWN] and self.raquete2_y + self.raquete_velocidade < ALTURA - ALTURA_RAQUETE:
            self.raquete2_y += self.raquete_velocidade

    def movimenta_bola(self):
        # Movimento da bola
        self.bola_x += self.bola_dx
        self.bola_y += self.bola_dy

        # Colisão das raquetes com a bola
        if (self.bola_dx < 0 and self.raquete1_y < self.bola_y < self.raquete1_y + self.player1.altura_raquete and RAIO_BOLA < self.bola_x < RAIO_BOLA + self.player1.largura_raquete):
            self.player1.sorteia_poder()
            self.bola_dx *= -1
        elif (self.bola_dx > 0 and self.raquete2_y < self.bola_y < self.raquete2_y + self.player2.altura_raquete and LARGURA - RAIO_BOLA - self.player2.largura_raquete < self.bola_x < LARGURA - RAIO_BOLA):
            self.player2.sorteia_poder()
            self.bola_dx *= -1

        # Colisão da bola com a tela
        if self.bola_y - RAIO_BOLA < 0 or self.bola_y + RAIO_BOLA > ALTURA:
            self.bola_dy *= -1

        # Pontuação
        if self.bola_x - RAIO_BOLA < 0:
            self.player2.score += 1
            self.reseta_bola(2, self.player1.score, self.player2.score)
        if self.bola_x + RAIO_BOLA > LARGURA:
            self.player1.score += 1
            self.reseta_bola(1, self.player1.score, self.player2.score)

    def renderiza_jogo(self):
        self.win.fill((0, 0, 0))
        pygame.draw.rect(self.win, self.player1.cor_raquete, pygame.Rect(0, self.raquete1_y, self.player1.largura_raquete, self.player1.altura_raquete))
        pygame.draw.rect(self.win, self.player2.cor_raquete, pygame.Rect(LARGURA - self.player2.largura_raquete, self.raquete2_y, self.player2.largura_raquete, self.player2.altura_raquete))
        pygame.draw.circle(self.win, WHITE, (self.bola_x, self.bola_y), RAIO_BOLA)
        score_text = self.font.render(f'{self.player1.score} - {self.player2.score}', True, WHITE)
        self.win.blit(score_text, (LARGURA // 2 - score_text.get_width() // 2, 30))
        pygame.display.flip()

    def reseta_bola(self, player, score1, score2):
        if player == 1 and score1 % 5 == 0:
            self.tela_de_vitoria(self.player1)
        elif player == 2 and score2 % 5 == 0:
            self.tela_de_vitoria(self.player2)
        
        self.bola_x, self.bola_y = LARGURA // 2, ALTURA // 2

    def tela_de_vitoria(self, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.bola_dx *= 1.1
                        self.bola_dy *= 1.1
                        self.raquete_velocidade *= 1.2
                        return  # Continua o jogo
                    elif event.key == pygame.K_c: # Grava a pontuação e sai
                        player.gravar_pontos()
                        pygame.quit()
                        sys.exit()

            self.win.fill((0, 0, 0))
            text = self.font.render(f'Parabéns {player.name}!', True, GREEN)
            self.win.blit(text, (LARGURA // 2 - text.get_width() // 2, ALTURA // 2 - text.get_height() // 2))
            text = self.font.render('Aperte G para continuar ou C para sair', True, WHITE)
            self.win.blit(text, (LARGURA // 2 - text.get_width() // 2, ALTURA // 2 - text.get_height() // 2 + TAMANHO_FONTE))
            pygame.display.flip()
            self.clock.tick(FPS)

class Player:
    def __init__(self, name, tipo):
        self.name = name
        self.score = 0
        self.poder = 'nenhum'
        self.cor_raquete = WHITE
        self.altura_raquete = 80
        self.largura_raquete = 15
        self.ultimo = 0

    def gravar_pontos(self):
        with open('scores.txt', 'a') as f:
            f.write(f'{self.name}: {self.score}\n')

    def sorteia_poder(self):
        if self.poder == 'nenhum':
            if True:
                tipo = 2
                if tipo == 1:
                    self.poder = 'inverte'
                    self.cor_raquete = GREEN
                elif tipo == 2:
                    self.poder = 'reduz'
                    self.altura_raquete = 40
                    self.cor_raquete = RED
                elif tipo == 3:
                    self.poder = 'aumenta'
                    self.altura_raquete = 100
                    self.cor_raquete = BLUE
        else:
            if self.ultimo == 2:
                self.poder = 'nenhum'
                self.altura_raquete = 80
                self.cor_raquete = WHITE
            else:
                self.ultimo += 1

class Menu:
    def __init__(self, win, clock, font):
        self.win = win
        self.clock = clock
        self.font = font

    def renderiza_tela(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: # Modo principal do jogo
                        game = Game(self.win, self.clock, self.font)
                        game.play()
                    elif event.key == pygame.K_c: # Placar (Não implementado)
                        pass 
                    elif event.key == pygame.K_m: # Multiplayer (Não implementado)
                        pass 

            self.win.fill((0, 0, 0))
            self.menu_principal()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def menu_principal(self):
        textos = ['Pong!!!', 'Aperte G para jogar', 'Aperte C para o placar', 'Aperte M para multiplayer']
        for i, txt in enumerate(textos):
            text = self.font.render(txt, True, WHITE)
            self.win.blit(text, (LARGURA // 2 - text.get_width() // 2, ALTURA // 2 - text.get_height() // 2 + i * TAMANHO_FONTE))

def main():
    pygame.init()
    win = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, TAMANHO_FONTE)
    menu = Menu(win, clock, font)
    menu.renderiza_tela()

if __name__ == "__main__":
    main()