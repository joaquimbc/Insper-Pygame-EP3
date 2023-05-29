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
    def __init__(self, win, clock, font, tipo):
        self.win = win
        self.clock = clock
        self.font = font
        self.bola_dx, self.bola_dy = 3, 3
        self.raquete_velocidade = 4
        self.score1, self.score2 = 0, 0
        self.bola_x, self.bola_y = LARGURA // 2, ALTURA // 2
        self.raquete1_y, self.raquete2_y = ALTURA // 2, ALTURA // 2
        self.raquete3_x, self.raquete4_x = LARGURA // 2, LARGURA // 2
        self.som_colisao = pygame.mixer.Sound('colisao.mp3')
        self.musica = pygame.mixer.Sound('musica_jogo.mp3')
        self.musica.play()
        self.tipo = tipo
        self.player1 = Player("Player 1", 'vertical')
        self.player2 = Player("Player 2", 'vertical')
        if self.tipo == 'quatro':
            self.player3 = Player("Player 3", 'horizontal')
            self.player4 = Player("Player 4", 'horizontal')

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

        if self.player1.poder == 'inverte':
            if keys[pygame.K_s] and self.raquete1_y - self.raquete_velocidade > 0:
                self.raquete1_y -= self.raquete_velocidade
            if keys[pygame.K_w] and self.raquete1_y + self.raquete_velocidade < ALTURA - self.player1.altura_raquete:
                self.raquete1_y += self.raquete_velocidade
        else:
            if keys[pygame.K_w] and self.raquete1_y - self.raquete_velocidade > 0:
                self.raquete1_y -= self.raquete_velocidade
            if keys[pygame.K_s] and self.raquete1_y + self.raquete_velocidade < ALTURA - self.player1.altura_raquete:
                self.raquete1_y += self.raquete_velocidade

        if self.player2.poder == 'inverte':
            if keys[pygame.K_DOWN] and self.raquete2_y - self.raquete_velocidade > 0:
                self.raquete2_y -= self.raquete_velocidade
            if keys[pygame.K_UP] and self.raquete2_y + self.raquete_velocidade < ALTURA - self.player2.altura_raquete:
                self.raquete2_y += self.raquete_velocidade
        else:
            if keys[pygame.K_UP] and self.raquete2_y - self.raquete_velocidade > 0:
                self.raquete2_y -= self.raquete_velocidade
            if keys[pygame.K_DOWN] and self.raquete2_y + self.raquete_velocidade < ALTURA - self.player2.altura_raquete:
                self.raquete2_y += self.raquete_velocidade

        if self.tipo == 'quatro':
            if self.player3.poder == 'inverte':
                if keys[pygame.K_c] and self.raquete3_x - self.raquete_velocidade > 0:
                    self.raquete3_x -= self.raquete_velocidade
                if keys[pygame.K_x] and self.raquete3_x + self.raquete_velocidade < LARGURA - self.player3.altura_raquete:
                    self.raquete3_x += self.raquete_velocidade
            else:
                if keys[pygame.K_x] and self.raquete3_x - self.raquete_velocidade > 0:
                    self.raquete3_x -= self.raquete_velocidade
                if keys[pygame.K_c] and self.raquete3_x + self.raquete_velocidade < LARGURA - self.player3.altura_raquete:
                    self.raquete3_x += self.raquete_velocidade
            
            if self.player4.poder == 'inverte':
                if keys[pygame.K_m] and self.raquete4_x - self.raquete_velocidade > 0:
                    self.raquete4_x -= self.raquete_velocidade
                if keys[pygame.K_n] and self.raquete4_x + self.raquete_velocidade < LARGURA - self.player4.altura_raquete:
                    self.raquete4_x += self.raquete_velocidade
            else:
                if keys[pygame.K_n] and self.raquete4_x - self.raquete_velocidade > 0:
                    self.raquete4_x -= self.raquete_velocidade
                if keys[pygame.K_m] and self.raquete4_x + self.raquete_velocidade < LARGURA - self.player4.altura_raquete:
                    self.raquete4_x += self.raquete_velocidade

    def movimenta_bola(self):
        # Movimento da bola
        self.bola_x += self.bola_dx
        self.bola_y += self.bola_dy

        # Colisão das raquetes com a bola
        # Colisão das raquetes com a bola
        if (self.bola_dx < 0 and self.raquete1_y < self.bola_y < self.raquete1_y + self.player1.altura_raquete and RAIO_BOLA < self.bola_x < RAIO_BOLA + self.player1.largura_raquete):
            self.player1.sorteia_poder()
            self.som_colisao.play()
            self.bola_dx *= -1
        elif (self.bola_dx > 0 and self.raquete2_y < self.bola_y < self.raquete2_y + self.player2.altura_raquete and LARGURA - RAIO_BOLA - self.player2.largura_raquete < self.bola_x < LARGURA - RAIO_BOLA):
            self.player2.sorteia_poder()
            self.som_colisao.play()
            self.bola_dx *= -1
        if self.tipo == 'quatro':
            if (self.bola_dy < 0 and self.raquete3_x < self.bola_x < self.raquete3_x + self.player3.altura_raquete and RAIO_BOLA < self.bola_y < RAIO_BOLA + self.player3.largura_raquete):
                self.player3.sorteia_poder()
                self.som_colisao.play()
                self.bola_dy *= -1
            elif (self.bola_dy > 0 and self.raquete4_x < self.bola_x < self.raquete4_x + self.player4.altura_raquete and ALTURA - RAIO_BOLA - self.player4.largura_raquete < self.bola_y < ALTURA - RAIO_BOLA):
                self.player4.sorteia_poder()
                self.som_colisao.play()
                self.bola_dy *= -1

        # Colisão da bola com a tela
        if self.tipo == 'dois':
            if self.bola_y - RAIO_BOLA < 0 or self.bola_y + RAIO_BOLA > ALTURA:
                self.som_colisao.play()
                self.bola_dy *= -1

        # Pontuação
        if self.bola_x - RAIO_BOLA < 0:
            self.player2.score += 1
            self.reseta_bola(2, self.player1.score, self.player2.score)
        if self.bola_x + RAIO_BOLA > LARGURA:
            self.player1.score += 1
            self.reseta_bola(1, self.player1.score, self.player2.score)
        if self.tipo == 'quatro':	
            if self.bola_y - RAIO_BOLA < 0:	
                self.player4.score += 1	
                self.reseta_bola(4, self.player3.score, self.player4.score)	
            if self.bola_y + RAIO_BOLA > ALTURA:	
                self.player3.score += 1	
                self.reseta_bola(3, self.player3.score, self.player4.score)

    def renderiza_jogo(self):
        self.win.fill((0, 0, 0))
        pygame.draw.rect(self.win, self.player1.cor_raquete, pygame.Rect(0, self.raquete1_y, self.player1.largura_raquete, self.player1.altura_raquete))
        pygame.draw.rect(self.win, self.player2.cor_raquete, pygame.Rect(LARGURA - self.player2.largura_raquete, self.raquete2_y, self.player2.largura_raquete, self.player2.altura_raquete))
        if self.tipo == 'quatro':
            pygame.draw.rect(self.win, self.player3.cor_raquete, pygame.Rect(self.raquete3_x, 0, self.player3.altura_raquete, self.player3.largura_raquete))
            pygame.draw.rect(self.win, self.player4.cor_raquete, pygame.Rect(self.raquete4_x, ALTURA - self.player4.largura_raquete, self.player4.altura_raquete, self.player4.largura_raquete))
        pygame.draw.circle(self.win, WHITE, (self.bola_x, self.bola_y), RAIO_BOLA)
        if self.tipo == 'quatro':
            score_text = self.font.render(f'P1:{self.player1.score} - P2:{self.player2.score} - P3:{self.player3.score} - P4:{self.player4.score}', True, WHITE)
        else:
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
        self.tipo = tipo
        self.ultimo = 0

    def gravar_pontos(self):
        with open('scores.txt', 'a') as f:
            f.write(f'{self.name}: {self.score}\n')

    def sorteia_poder(self):
        if self.poder == 'nenhum':
            if True:
                tipo = 1
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
        pygame.mixer.init()
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
                        game = Game(self.win, self.clock, self.font, 'dois')
                        game.play()
                    elif event.key == pygame.K_c: # Placar (Não implementado)
                        pass 
                    elif event.key == pygame.K_v: # Quatro jogadores
                        game = Game(self.win, self.clock, self.font, 'quatro')
                        game.play()

            self.win.fill((0, 0, 0))
            self.menu_principal()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def menu_principal(self):
        textos = ['Pong!!!', 'Aperte G para jogar', 'Aperte C para o placar', 'Aperte V Para quatro jogadores']
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