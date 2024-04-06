import pygame
import sys
from os import walk, path, getcwd


class LibrasGame:
    def __init__(self):
        self.DIR = getcwd()
        self.bar = '/' if '/' in self.DIR else '\\'
        self.DIR += self.bar

        self.load_images = {
            "sinais": [],
            "start": pygame.image.load(self.DIR + 'img' + self.bar + 'start_img_game.png'),
            "start_questions": pygame.image.load(self.DIR + 'img' + self.bar + 'answers_img_game.png'),
            "life0": pygame.image.load(self.DIR + 'img' + self.bar + 'life_img_0.jpg'),
            "life1": pygame.image.load(self.DIR + 'img' + self.bar + 'life_img_1.jpg'),
            "end0": pygame.image.load(self.DIR + 'img' + self.bar + 'end_img_game.png'),
            "end1": pygame.image.load(self.DIR + 'img' + self.bar + 'win_img_game.png'),
        }

        # Declaração de super variáveis
        self.TIMER = 60
        self.START = False
        self.START_QUESTIONS = False
        self.CHEAT = True  # 'True', caso queira aumentar as vidas teclando SHIFT
        self.LIFE = 10
        self.hp = self.LIFE
        print(self.LIFE)

        pygame.init()

        # Declaração da variável responsável pelo update da janela
        self.clock = pygame.time.Clock()

        # Configurações da janela
        self.screen = pygame.display.set_mode([600, 500])
        pygame.display.set_caption('Jogo da Linguagem de Sinais')

        # Definições de fontes do pygame
        self.base_font = pygame.font.Font(None, 32)
        self.user_text = ''
        self.time_text = ''

        # Definições de retângulos do pygame
        self.input_rect = pygame.Rect(250, 400, 140, 32)
        self.time_rect = pygame.Rect(50, 400, 50, 50)

        # Definições de cor do retângulo principal
        self.color_active = pygame.Color('lightskyblue3')
        self.color_error = pygame.Color('brown1')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False
        self.error = False

        # Definição da música de fundo da entrada
        pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'minecraft.mp3')
        pygame.mixer.music.play()  # loops=-1 (padrão) => faz a música se repetir indefinidamente

    def resp_config(self):
        # Definições das respostas e das imagens das questões
        self.nomes_sinal = []
        self.sinais = []
        qtd_sinais = 0
        for a, b, i in walk(self.DIR + 'sinais_img'):
            for c in i:
                self.sinais.append(path.join(a, c))
            self.nomes_sinal = i
            qtd_sinais = len(i)

        self.atual_sinal = 0  # Variável responsável pelo relacionamento entre a resposta e a imagem exibida
        self.resp = self.nomes_sinal[self.atual_sinal][:-4]
        for s in range(qtd_sinais):
            sin = pygame.image.load(self.sinais[s]).convert_alpha()
            w, h = sin.get_size()
            sin = pygame.transform.smoothscale(sin, (int(w * 2), int(h * 2)))
            self.load_images['sinais'].append(sin)


        self.pos_sinal = (160, 50)

    def life_system(self, current_life):
        # Definição da imagem do coraçãozinho
        life_img = []
        for index_life in range(2):
            img_l = self.load_images[f"life{index_life}"].convert_alpha()
            w_life, h_life = img_l.get_size()
            img_l = pygame.transform.smoothscale(img_l, (int(w_life * 0.5), int(h_life * 0.5)))
            life_img.append(img_l)

        # Os corações são espaçados em 36 e terminam na qtd de corações (menos o primeiro) vezes o número do espaçamento + a
        # posição do primeiro + 1 (pra contar no range)
        pos_x_life = [x for x in range(3, (36 * (self.LIFE - 1) + 4), 36)]
        self.pos_life = {'x': pos_x_life, 'y': 3}

        dead = self.LIFE - current_life
        for i in range(current_life):
            self.screen.blit(life_img[1], (self.pos_life['x'][i], self.pos_life['y']))
        for j in range(1, dead + 1):
            self.screen.blit(life_img[0], (self.pos_life['x'][-j], self.pos_life['y']))

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def start_status(self):
        # Definições e verifição sobre o início do game
        start_img = self.load_images['start']
        pos_start = (25, 0)

        while not self.START:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.START = True

            self.screen.blit(start_img, pos_start)
            pygame.display.flip()
            self.clock.tick(60)

        answers_img = self.load_images['start_questions']
        pos_answers = (0, 0)

        while not self.START_QUESTIONS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Tira a música de fundo do início
                        pygame.mixer.music.unload()
                        # Definição do efeito quando começa o game
                        pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'go_start.wav')
                        pygame.mixer.music.play()

                        self.START_QUESTIONS = True

            self.screen.blit(answers_img, pos_answers)
            pygame.display.flip()
            self.clock.tick(60)

    def end(self, final=0):
        # A imagem de end_0_img é a padrão, caso nada seja passado por parâmetro
        end_0_img = self.load_images['end0']
        end_1_img = self.load_images['end1']
        pos_end = (25, 0)

        while True:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.quit_game()

            if final == 1:  # Plota a imagem de vitória
                self.screen.blit(end_1_img, pos_end)
            else:
                self.screen.blit(end_0_img, pos_end)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.screen.fill((255, 255, 255))

        self.resp_config()
        self.start_status()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False

                if event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        # Faz a verificação da resposta
                        if self.user_text.strip().lower() == self.resp.lower():  # Se estiver correta, ele vai para a próxima questão
                            self.atual_sinal += 1
                            try:
                                self.sinal = self.load_images['sinais'][self.atual_sinal]
                            except IndexError:
                                # Definição do efeito de vitória
                                pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'win.wav')
                                pygame.mixer.music.play()
                                self.end(1)
                            self.resp = self.nomes_sinal[self.atual_sinal][:-4]
                            self.user_text = ''
                            self.error = False
                        else:  # Se estiver errada, ele reduz uma chance
                            self.hp -= 1
                            print(self.hp)
                            if self.hp <= 0:  # Encerra o jogo quando as chances acabam
                                # Definição do efeito de derrota
                                pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'defeat.wav')
                                pygame.mixer.music.play()
                                self.end(0)
                            # Definição do efeito de resposta incorreta
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'negative.wav')
                            pygame.mixer.music.play()
                            self.error = True
                    # Ao teclar em SHIFT, ganha uma vida >> Deve mudar o estado da variável 'CHEAT' para 'True'
                    if (event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT) and self.CHEAT:
                        if self.hp < self.LIFE:
                            self.hp += 1

                    # Sistema de deletar caracteres no retângulo principal
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]

                    # Sistema de adicionar caracteres no retângulo principal
                    elif event.key != pygame.K_RETURN:
                        pygame.mixer.music.load(self.DIR + 'musics' + self.bar + 'snap_lofi.wav')
                        pygame.mixer.music.play()
                        self.user_text += event.unicode

                    else:
                        pass

            self.screen.fill((255, 255, 255))
            # Plotagem da imagem da questão
            self.screen.blit(self.load_images['sinais'][self.atual_sinal], self.pos_sinal)

            # Sistema de plotagem das imagens dos coraçõezinhos
            self.life_system(self.hp)

            # altera a cor quando pressionado, quando a resposta é incorreta ou quando não está pressionado o retângulo da resp
            if self.active and not self.error:
                color = self.color_active
            elif self.error and self.active:
                color = self.color_error
            else:
                color = self.color_passive

            # Exibição do retângulo principal
            pygame.draw.rect(self.screen, color, self.input_rect)
            # Definição do texto digitado para futura plotagem
            text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
            # Plotagem do texto digitado no retângulo principal
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            # Altera o comprimento do retângulo principal de acordo com o tamanho do texto digitado
            self.input_rect.w = max(100, text_surface.get_width() + 10)

            pygame.display.flip()
            self.clock.tick(40)


if __name__ == '__main__':
    lg = LibrasGame()
    lg.run()
