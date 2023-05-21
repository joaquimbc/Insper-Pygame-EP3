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
        pass

class Player:
    def __init__(self, name, tipo):
        pass

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
        pass

def main():
    print("Ola!")

if __name__ == "__main__":
    main()