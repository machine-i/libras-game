import pygame
import sys
from os import walk, path

# Declaração de super variáveis
TIMER = 60
START = False
START_QUESTIONS = False
CHEAT = True  # Mude para 'True', caso queira aumentar as vidas teclando SHIFT
LIFE = 5  # Vidas
print(LIFE)  # Apenas para debug

pygame.init()

# Declaração da variável responsável pelo update da janela
clock = pygame.time.Clock()

# Configurações da janela
screen = pygame.display.set_mode([600, 500])
pygame.display.set_caption('Jogo da Linguagem de Sinais')

# Definições de fontes do pygame
base_font = pygame.font.Font(None, 32)
user_text = ''
time_text = ''

# Definições de retângulos do pygame
input_rect = pygame.Rect(250, 250, 140, 32)
time_rect = pygame.Rect(50, 400, 50, 50)

# Definições de cor do retângulo principal
color_active = pygame.Color('lightskyblue3')
color_error = pygame.Color('brown1')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False
error = False

# Definições das respostas e das imagens das questões
nomes_sinal = []
sinais = []
for a, b, i in walk('/home/rene/Documentos/rene/_myProjects/libras_game/sinais_img'):
    for c in i:
        sinais.append(path.join(a, c))
    nomes_sinal = i

atual_sinal = 0  # Variável responsável pelo relacionamento entre a resposta e a imagem exibida
resp = nomes_sinal[atual_sinal][:-4]
sinal = pygame.image.load(sinais[atual_sinal]).convert_alpha()
w, h = sinal.get_size()
sinal = pygame.transform.smoothscale(sinal, (int(w*2), int(h*2)))
pos_sinal = (160, 50)

# Definição da música de fundo da entrada
pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/minecraft.mp3')
pygame.mixer.music.play()  # loops=-1 (padrão) => faz a música se repetir indefinidamente

# Definição da imagem do coraçãozinho
life_img = []
for f in range(2):
    img_l = pygame.image.load('/home/rene/Documentos/rene/_myProjects/libras_game/img/life_img_'+str(f)+'.jpg').convert_alpha()
    w_life, h_life = img_l.get_size()
    img_l = pygame.transform.smoothscale(img_l, (int(w_life*0.5), int(h_life*0.5)))
    life_img.append(img_l)

# Declaração das variáveis de Hit Point e de posição dos coraçõezinhos
hp = LIFE
pos_x_life = [x for x in range(3, (36*(LIFE-1)+4), 36)]  # Gera posições que iniciam em 3 e variam num espaço de 36. A equação do término do "range" usa do produto entre o step de 36 e o número de vidas -1, somando da posição do primeiro coraçãozinho +1 (porque o stop do "range" não é retornado).
pos_life = {'x': pos_x_life, 'y': 3}

# Função responsável pela plotagem das imagens dos coraçõezinhos, fazendo a análise das quantidades de chances restantes
def life_system(hp):
    dead = LIFE - hp
    for i in range(hp):
        screen.blit(life_img[1], (pos_life['x'][i], pos_life['y']))
    for j in range(1, dead + 1):
        screen.blit(life_img[0], (pos_life['x'][-j], pos_life['y']))

# Função responsável por fechar o game
def quitGame():
    pygame.quit()
    sys.exit()

# Definições e verifição sobre o início do game
start_img = pygame.image.load('/home/rene/Documentos/rene/_myProjects/libras_game/img/start_img_game.png')
pos_start = (25, 0)
def start():
    global START
    while not START:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START = True  # Caso o usuário clique no espaço, o programa sai do loop local infinito e continua no loop principal

        screen.blit(start_img, pos_start)
        pygame.display.flip()
        clock.tick(60)

answers_img = pygame.image.load('/home/rene/Documentos/rene/_myProjects/libras_game/img/answers_img_game.png')
pos_answers = (60, 0)
def answers():
    global START_QUESTIONS
    while not START_QUESTIONS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Tira a música de fundo do início
                    pygame.mixer.music.unload()
                    # Definição do efeito quando começa o game
                    pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/go_start.wav')
                    pygame.mixer.music.play()

                    START_QUESTIONS = True  # Caso o usuário clique no espaço, o programa sai do loop local infinito e continua no loop principal

        screen.blit(answers_img, pos_answers)
        pygame.display.flip()
        clock.tick(60)

# Definições e verifição sobre o fim do game (basicamente plota uma imagem na tela e fica esperando o usuário clicar no espaço ou no "X" da janela)
end_0_img = pygame.image.load('/home/rene/Documentos/rene/_myProjects/libras_game/img/end_img_game.png')
end_1_img = pygame.image.load('/home/rene/Documentos/rene/_myProjects/libras_game/img/win_img_game.png')
pos_end = (25, 0)
def end(final=0):  # A imagem de end_0_img é a padrão, caso nada seja passado por parâmetro
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quitGame()

        if final == 1:  # Plota a imagem de vitória
            screen.blit(end_1_img, pos_end)
        else:
            screen.blit(end_0_img, pos_end)
        pygame.display.flip()
        clock.tick(60)

# Loop principal
while True:
    # Estabele uma cor de fundo da janela
    screen.fill((255, 255, 255))

    # Entra no loop local infinito e espera até que o usuário queira iniciar o game
    start()

    answers()

    # Definições sobre o tempo do game
    # time_now = pygame.time.get_ticks() // 1000
    # time_reg = TIMER - time_now
    # if time_reg <= -1:
    #     quitGame()

    # Configurações sobre qualquer evento que aconteca na janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN and active:
            # Faz a verificação da resposta
            if event.key == pygame.K_SPACE:
                if user_text.strip() == resp:  # Se estiver correta, ele vai para a próxima questão
                    atual_sinal += 1
                    try:
                        sinal = pygame.image.load(sinais[atual_sinal]).convert_alpha()
                    except IndexError:
                        # Definição do efeito de vitória
                        pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/win.wav')
                        pygame.mixer.music.play()
                        end(1)
                    w, h = sinal.get_size()
                    sinal = pygame.transform.smoothscale(sinal, (int(w*2), int(h*2)))
                    resp = nomes_sinal[atual_sinal][:-4]
                    user_text = ''
                    error = False
                else:  # Se estiver errada, ele reduz uma chance
                    hp -= 1
                    print(hp)
                    if hp <= 0:  # Encerra o game quando as chances acabam
                        # Definição do efeito de derrota
                        pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/defeat.wav')
                        pygame.mixer.music.play()
                        end(0)
                    # Definição do efeito de resposta incorreta
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/negative.wav')
                    pygame.mixer.music.play()
                    error = True
            # Ao teclar em SHIFT, ganha uma vida >> Deve mudar o estado da variável 'CHEAT' para 'True'
            if (event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT) and CHEAT:
                if hp < LIFE:
                    hp += 1

            # Sistema de deletar caracteres no retângulo principal
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

            # Sistema de adicionar caracteres no retângulo principal
            elif event.key != pygame.K_SPACE:
                pygame.mixer.music.load('/home/rene/Documentos/rene/_myProjects/libras_game/musics/snap_lofi.wav')
                pygame.mixer.music.play()
                user_text += event.unicode

            else:
                pass

    # Plotagem da imagem da questão
    screen.blit(sinal, pos_sinal)

    # Sistema de plotagem das imagens dos coraçõezinhos
    life_system(hp)

    # time_text = str(time_reg)
    # print(time_reg)

    # Verificação do estado do retângulo principal (altera a cor quando pressionado, quando a resposta é incorreta ou quando não está pressionado)
    if active and not error:
        color = color_active
    elif error and active:
        color = color_error
    else:
        color = color_passive
    
    # Exibição do retângulo principal
    pygame.draw.rect(screen, color, input_rect)
    # Definição do texto digitado para futura plotagem
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    # Plotagem do texto digitado no retângulo principal
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width()+10)  # Altera o comprimento do retângulo principal de acordo com o tamanho do texto digitado

    # Exibição do retângulo do tempo
    # pygame.draw.rect(screen, color_active, time_rect)
    # Definição do tempo para futura plotagem
    # time_show = base_font.render(time_text, True, (255, 255, 255))
    # Plotagem do tempo no retângulo do tempo
    # screen.blit(time_show, (time_rect.x+19, time_rect.y+15))
      
    pygame.display.flip()
    clock.tick(40)
