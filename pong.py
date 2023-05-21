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
        pass

    def movimenta_raquete(self):
        pass

    def movimenta_bola(self):
        pass

    def renderiza_jogo(self):
        pass

    def reseta_bola(self, player, score1, score2):
        pass

    def tela_de_vitoria(self, player):
        pass

class Player:
    def __init__(self, name, tipo):
        self.name = name
        self.score = 0

    def gravar_pontos(self):
        with open('scores.txt', 'a') as f:
            f.write(f'{self.name}: {self.score}\n')

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
                        pass
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