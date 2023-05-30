import sys
import pygame
from random import randint
from pygame_textinput import digita_nome # Código pego de https://github.com/Nearoo/pygame-text-input

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
    """
    A classe Game é responsável praticamente pelo jogo inteiro. É composta por várias funções, desde colisões,
    movimentar a bola, ou mostrar o placar de vitória. Em retrospectiva, eu deveria ter feito ela mais "quebrada",
    separando suas várias funções em classes diferentes (como as raquetes, bola, tela de vitória etc) mas enfim, não da mais tempo infezlimente

    A classe Game conta com as seguintes variáveis:

    # win - A tela do jogo
    # clock - 
    # font - A fonte do jogo
    # bola_bx, bola_dy - A velocidade da bola no eixo X e Y, respectivamente
    # bola_x, bola_y - As posições da bola no eixo X e Y, respectiavemente
    # raquete_velocidade - A velocidade da raquete 
    # raquete@_x, raquete@_y - É a posição das raquetes para cada jogador. Como queremos ela no meio, elas iniciam na metade da altura (ou largura)
    # som_colisao - O som que é tocado quando a bola colide com algo
    # musica - A música de fundo do jogo (tá mal implementado, mas funciona...)
    # tipo - Define se o jogo é de dois jogadores ou de quatro jogadores
    # ultima_pontuacao - Um dicionário que guarda quais foram a última vez que cada jogador atingiu a pontuação necessária para a tela de vitória
    # player@ - São os objetos dos jogadores. Levam como argumento seu nome (que deve ser digitado pelo usuário)
    """
    def __init__(self, win, clock, font, tipo):
        self.win = win
        self.clock = clock
        self.font = font
        self.bola_dx, self.bola_dy = 3, 3
        self.bola_x, self.bola_y = LARGURA // 2, ALTURA // 2
        self.raquete_velocidade = 4
        self.raquete1_y, self.raquete2_y = ALTURA // 2, ALTURA // 2
        self.raquete3_x, self.raquete4_x = LARGURA // 2, LARGURA // 2
        self.som_colisao = pygame.mixer.Sound('colisao.mp3')
        self.musica = pygame.mixer.Sound('musica_jogo.mp3')
        self.musica.play()
        self.tipo = tipo
        self.ultima_pontuacao = {} 
        self.player1 = Player(digita_nome(1))
        self.player2 = Player(digita_nome(2))
        if self.tipo == 'quatro':
            self.player3 = Player(digita_nome(3))
            self.player4 = Player(digita_nome(4))

    def play(self):
        """
        Loop principal do jogo
        """
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
        """
        É a função responsável por movimentar a raquete pela tela. Os controles são invertidos quando o poder 'inverte' está ativado
        A posição da raquete no eixo em que deve se movimentar é atualizada de acordo com sua velocidade
        Tá bem feia, mas tá funcional...
        """
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
        """
        Uma das funções mais importantes. Provavelmente deveria se chamar outra coisa, mas já esta aqui né. Ela possui 3 funções principais:

        1 - Movimentar a bola pela tela
        2 - Detectar colisões da bola tanto com as raquetes, tanto que com a tela
            PS: Por conta da implemetação, as dimensões das raquetes horizontais estão invertidas. Não é um bug
        3 - Detectar quando uma bola saiu da tela, e contabilizar pontos para quem o marcou
            PS: Por conta da implementação, quando jogando em 4 jogadores, você só pode fazer pontos se a bola passar pela 'vala' do jogador oposto a você
        """
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
            self.reseta_bola(2)
        if self.bola_x + RAIO_BOLA > LARGURA:
            self.player1.score += 1
            self.reseta_bola(1)
        if self.tipo == 'quatro':	
            if self.bola_y - RAIO_BOLA < 0:	
                self.player4.score += 1	
                self.reseta_bola(4)	
            if self.bola_y + RAIO_BOLA > ALTURA:	
                self.player3.score += 1	
                self.reseta_bola(3)

    def renderiza_jogo(self):
        """
        Como o nome já diz, é responsável por renderizar todos os elementos do jogo. Os pontos, as raquetes e a bola
        Está bem 'cru', provavelmente deveríamos ter apostado em coisas como sprites ao invés de desenhar tudo na mão, mas por mais feio que esteja, funciona mesmo assim

        PS: As orientações das raquetes horizontais estão invertidas. Não é um bug
        """
        self.win.fill((0, 0, 0))
        pygame.draw.rect(self.win, self.player1.cor_raquete, pygame.Rect(0, self.raquete1_y, self.player1.largura_raquete, self.player1.altura_raquete))
        pygame.draw.rect(self.win, self.player2.cor_raquete, pygame.Rect(LARGURA - self.player2.largura_raquete, self.raquete2_y, self.player2.largura_raquete, self.player2.altura_raquete))
        if self.tipo == 'quatro':
            pygame.draw.rect(self.win, self.player3.cor_raquete, pygame.Rect(self.raquete3_x, 0, self.player3.altura_raquete, self.player3.largura_raquete))
            pygame.draw.rect(self.win, self.player4.cor_raquete, pygame.Rect(self.raquete4_x, ALTURA - self.player4.largura_raquete, self.player4.altura_raquete, self.player4.largura_raquete))
        pygame.draw.circle(self.win, WHITE, (self.bola_x, self.bola_y), RAIO_BOLA)
        if self.tipo == 'quatro':
            score_text = self.font.render(f'{self.player1.name}: {self.player1.score} -{self.player2.name}: {self.player2.score} - {self.player3.name}: {self.player3.score} - {self.player4.name}: {self.player4.score}', True, WHITE)
        else:
            score_text = self.font.render(f'{self.player1.name}: {self.player1.score} - {self.player2.name}: {self.player2.score}', True, WHITE)
        self.win.blit(score_text, (LARGURA // 2 - score_text.get_width() // 2, 30))
        pygame.display.flip()

    def reseta_bola(self, player):
        """
        Essa função possuí 2 trabalhos praticamente:

        1 - 'Devolver' a bola para o centro da tela quando um ponto é marcado
        2 - Ela verifica se o jogador que marcou o ponto já possui pontos o suficiente para a tela de vitória. Para isso, se é utilizado o dicionário
        ultima_pontuacao para contabilizar o avanço do jogo
        """
        if self.tipo == 'dois':
            for player in [self.player1, self.player2]:
                if player.score % 5 == 0 and self.ultima_pontuacao.get(player, 0) != player.score:
                    self.tela_de_vitoria(player)
                    self.ultima_pontuacao[player] = player.score
        else:
            for player in [self.player1, self.player2, self.player3, self.player4]:
                if player.score % 5 == 0 and self.ultima_pontuacao.get(player, 0) != player.score:
                    self.tela_de_vitoria(player)
                    self.ultima_pontuacao[player] = player.score
        
        self.bola_x, self.bola_y = LARGURA // 2, ALTURA // 2

    def tela_de_vitoria(self, player):
        """
        Se trata de uma função que sinceramente não deveria fazer parte da classe Game, mas enfim.
        Ela é quem é mostrada após algum jogador marcar 5 pontos. Após isso, ela irá ou sair do jogo e 
        gravar a maior pontuação em um arquivo (algo que eu só percebi que estava bugado até escrever isso rsrsrsrs)
        """
        if self.tipo == 'dois':
            jogadores = [self.player1, self.player2]
        else:
            jogadores = [self.player1, self.player2, self.player3, self.player4]
        # Determina o jogador com a maior pontuação (sério, eu deveria ter descoberto lambdas antes...)
        jogador_com_mais_pontos = max(jogadores, key=lambda jogador: jogador.score)

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
                        jogador_com_mais_pontos.gravar_pontos()
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
    """
    É a classe responsável por gerenciar os jogadores, seus poderes e o tamanho de suas raquetes. Possui como valores:

    # name - O nome do jogador
    # score - A atual pontuação do jogador
    # poder - O atual poder do jogador
    # cor_raquete - A cor da raquete do jogador
    # altura_raquete, largura_raquete - A largura e a altura da raquete do jogador
    # ultimo - Quantas rodadas desde a ativação do poder

    Note que por conta das raquetes horizontais serem praticamente a mesma coisa renderizadas ao contrário, não é necessário saber qual é qual,
    pois a altura de uma raquete horizontal corresponde a sua largura. É confuso, mas funciona
    """
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.poder = 'nenhum'
        self.cor_raquete = WHITE
        self.altura_raquete = 80
        self.largura_raquete = 15
        self.ultimo = 0

    def gravar_pontos(self):
        """
        Guarda os pontos do jogador no arquivo. Não sei se é o melhor lugar pra isso, mas já tá aqui né
        """
        with open('scores.txt', 'a') as f:
            f.write(f'{self.name}: {self.score}\n')

    def sorteia_poder(self):
        """
        É uma função que é chamada quando uma bola entra em colisão com uma raquete. Ela possuí algumas funções:

        1 - Sortear e aplicar o poder caso a raquete não tenha algum
        2 - Verificar se já se passaram turnos o suficiente para o poder sair

        Não é muito eficiente, pois os poderes duram mais do que deveriam (pois só podem ser desativados na colisão), porém faz um bom trabalho mesmo assim
        """
        if self.poder == 'nenhum':
            if randint(1,3) == 3:
                tipo = randint(1,3)
                if tipo == 1:
                    self.poder = 'inverte'
                    self.cor_raquete = GREEN
                elif tipo == 2:
                    self.poder = 'reduz'
                    self.altura_raquete = 40
                    self.cor_raquete = RED
                elif tipo == 3:
                    self.poder = 'aumenta'
                    self.altura_raquete = 110
                    self.cor_raquete = BLUE
        else:
            if self.ultimo == 2:
                self.poder = 'nenhum'
                self.altura_raquete = 80
                self.largura_raquete = 15
                self.cor_raquete = WHITE
            else:
                self.ultimo += 1

class Menu:
    """
    É a classe responsável pelo menu principal e pelo placar. Provavelmente aqui também deveria ter outras telas, como a de vitória, mas já foi
    Tem poucos valores em si, apenas a tela, a fonte e o clock.
    """
    def __init__(self, win, clock, font):
        self.win = win
        self.clock = clock
        self.font = font

    def verifica_opcao(self):
        """
        É a função que seleciona qual modo o jogador quer jogar. Também cria o background para menu_principal()
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: # Modo principal do jogo
                        game = Game(self.win, self.clock, self.font, 'dois')
                        game.play()
                    elif event.key == pygame.K_c: # Placar 
                        self.placar()
                    elif event.key == pygame.K_v: # Quatro jogadores
                        game = Game(self.win, self.clock, self.font, 'quatro')
                        game.play()

            self.win.fill((0, 0, 0))
            self.menu_principal()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def menu_principal(self):
        """
        O maior bode desse projeto x.x
        Desenha o menu principal do jogo inteiro. Ele é feio, horrível, horroroso, horripilante, nojento, mas não tem mais o que fazer
        Deveria ter feito mil melhorias, mas acabamos focando em outras partes que julgamos mais imporatentes
        Afinal de contas, pong nunca foi conhecido por seus belos gráficos ;)
        """
        textos = ['Pong!!!', 'Aperte G para jogar', 'Aperte C para o placar', 'Aperte V Para quatro jogadores']
        for i, txt in enumerate(textos):
            text = self.font.render(txt, True, WHITE)
            self.win.blit(text, (LARGURA // 2 - text.get_width() // 2, ALTURA // 2 - text.get_height() // 2 + i * TAMANHO_FONTE))

    def placar(self):
        """
        Exibe o placar de pontos APENAS caso haja pontos para serem exibidos. Se não, mostra que é necessário coletar pontos primeiro
        Ao contrário de praticamente todo esse projeto, dessa vez eu tentei ir com algo mais modular. E olha, ficou 10x melhor!
        Quem me dera restasse tempo para fazer todo o resto dessa forma...
        """
        # Fontes para o placar
        score_font = pygame.font.Font(None, 50)
        text_font = pygame.font.Font(None, 24)

        # Tenta ler as pontuações do arquivo scores.txt
        pontuacoes = self.carrega_pontos()

        # Se as pontuações não foram lidas, mostre uma mensagem e retorne
        if not pontuacoes:
            self.mostra_sem_pontos()
            return

        # Mostra o placar
        self.mostra_pontos(pontuacoes, text_font)


    def carrega_pontos(self):
        """
        Carrega os pontos do arquivo. Caso não haja pontos, irá ser retornado None
        """
        pontuacoes = []
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    player, pontos = line.strip().split(': ')
                    pontuacoes.append((player, int(pontos)))
            pontuacoes.sort(key=lambda x: x[1], reverse=True)
        except:
            pontuacoes = None
        return pontuacoes


    def mostra_sem_pontos(self):
        """
        A tela que é exibida quando não se tem pontuação ainda
        """
        while True:
            if self.quit():
                return

            self.win.fill((0,0,0))
            texto_titulo = self.font.render("Você ainda não possui pontos!", True, RED)
            titulo_rect = texto_titulo.get_rect(center=(LARGURA// 2, 60))
            self.win.blit(texto_titulo, titulo_rect)
            pygame.display.flip()


    def quit(self):
        """
        A função que retorna ao menu principal
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True
        return False


    def mostra_pontos(self, pontuacoes, text_font):
        """
        A função que mostra os pontos do arquivo na tela
        """
        while True:
            if self.quit():
                return

            self.win.fill((0,0,0))

            # Renderiza o título do placar
            texto_titulo = self.font.render("Placar", True, RED)
            titulo_rect = texto_titulo.get_rect(center=(LARGURA// 2, 60))
            self.win.blit(texto_titulo, titulo_rect)

            # Mostra a pontuação
            self.renderiza_pontos(pontuacoes)

            text = text_font.render("Pressione C para voltar ao menu principal", True, WHITE)
            text_rect = text.get_rect(center=(LARGURA // 2, ALTURA - 30))
            self.win.blit(text, text_rect)

            pygame.display.flip()


    def renderiza_pontos(self, pontuacoes):
        """
        Renderiza centralizadamente os pontos em si
        """
        y = 120
        for i, (player, pontos) in enumerate(pontuacoes):
            texto_jogador = self.font.render(f"{player}: {pontos}", True, WHITE)
            rect_jogador = texto_jogador.get_rect(center=(LARGURA // 2, y + i * 40))
            self.win.blit(texto_jogador, rect_jogador)


def main():
    """
    Função main de todo o jogo, não tem muito o que dizer
    """
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, TAMANHO_FONTE)
    menu = Menu(win, clock, font)
    menu.verifica_opcao()

if __name__ == "__main__":
    main()