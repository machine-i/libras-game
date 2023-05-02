import pygame
import sys
from os import walk

# Declaração de super variáveis
TIMER = 60
START = False
LIFE = 3  # Chances de errar
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

# Definições das respostas
nomes_sinal = []
for _, _, i in walk('/home/rene/Documentos/rene/python/libras_game/sinais_img'):
    nomes_sinal = i

# Definições das imagens das questões
sinais = [f'/home/rene/Documentos/rene/python/libras_game/sinais_img/{sinal_img}' for sinal_img in nomes_sinal]
atual_sinal = 0  # Variável responsável pelo relacionamento entre a resposta e a imagem exibida
sinal = pygame.image.load(sinais[atual_sinal]).convert_alpha()
w, h = sinal.get_size()
sinal = pygame.transform.smoothscale(sinal, (int(w*2), int(h*2)))
resp = nomes_sinal[atual_sinal][:-4]
pos_sinal = (160, 50)

# Definição da música de fundo
pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/minecraft.mp3')
pygame.mixer.music.play()  # loops=-1 (padrão) => faz a música se repetir indefinidamente

# Definição da imagem do coraçãozinho cheio
life_1_img = pygame.image.load('/home/rene/Documentos/rene/python/libras_game/life_img_1.jpg').convert_alpha()
w_life_1, h_life_1 = life_1_img.get_size()
life_1_img = pygame.transform.smoothscale(life_1_img, (int(w_life_1*0.5), int(h_life_1*0.5)))

# Definição da imagem do coraçãozinho vazio
life_0_img = pygame.image.load('/home/rene/Documentos/rene/python/libras_game/life_img_0.jpg').convert_alpha()
w_life_0, h_life_0 = life_0_img.get_size()
life_0_img = pygame.transform.smoothscale(life_0_img, (int(w_life_0*0.5), int(h_life_0*0.5)))

# Declaração das variáveis de Hit Point e de posição dos coraçõezinhos
hp = LIFE
pos_life = {'x': [3, 39, 75], 'y': 3}

# Função responsável pela plotagem das imagens dos coraçõezinhos, fazendo a análise das quantidades de chances restantes
def life_system(hp):
    dead = LIFE - hp
    for i in range(hp):
        screen.blit(life_1_img, (pos_life['x'][i], pos_life['y']))
    for j in range(1, dead + 1):
        screen.blit(life_0_img, (pos_life['x'][-j], pos_life['y']))

# Função responsável por fechar o game
def quitGame():
    pygame.quit()
    sys.exit()

# Definições e verifição sobre o início do game
start_img = pygame.image.load('/home/rene/Documentos/rene/python/libras_game/start_img_game.png')
pos_start = (25, 0)
def start():
    global START
    while not START:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Tira a música de fundo do início
                    pygame.mixer.music.unload()
                    # Definição do efeito quando começa o game
                    pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/go_start.wav')
                    pygame.mixer.music.play()

                    START = True  # Caso o usuário clique no espaço, o programa sai do loop local infinito e continua no loop principal

        screen.blit(start_img, pos_start)
        pygame.display.flip()
        clock.tick(60)

# Definições e verifição sobre o fim do game (basicamente plota uma imagem na tela e fica esperando o usuário clicar no espaço ou no "X" da janela)
end_0_img = pygame.image.load('/home/rene/Documentos/rene/python/libras_game/end_img_game.png')
end_1_img = pygame.image.load('/home/rene/Documentos/rene/python/libras_game/win_img_game.png')
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

        if event.type == pygame.KEYDOWN:
            # Faz a verificação da resposta
            if event.key == pygame.K_SPACE and active:
                if user_text.strip() == resp:  # Se estiver correta, ele vai para a próxima questão
                    atual_sinal += 1
                    try:
                        sinal = pygame.image.load(sinais[atual_sinal]).convert_alpha()
                    except IndexError:
                        # Definição do efeito de vitória
                        pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/win.wav')
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
                        pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/defeat.wav')
                        pygame.mixer.music.play()
                        end(0)
                    # Definição do efeito de resposta incorreta
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/negative.wav')
                    pygame.mixer.music.play()
                    error = True

            # Sistema de deletar caracteres no retângulo principal
            if event.key == pygame.K_BACKSPACE and active:
                user_text = user_text[:-1]

            # Sistema de adicionar caracteres no retângulo principal
            elif active and event.key != pygame.K_SPACE:
                pygame.mixer.music.load('/home/rene/Documentos/rene/python/libras_game/musics/snap_lofi.wav')
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
