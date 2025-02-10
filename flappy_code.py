# Ali Sabouri
# Welcom to My code
import pygame
import sys
import random
import time
#Start Pygame Modules
pygame.init()


#All Variable
display_width=576
display_height=1024
floor_x = 0
gravity = 0.25
bird_movment = 0
pipe_list = []
game_status = True
bird_list_index = 2
game_font = pygame.font.Font('F:/flatybird/font/Flappy.TTF', 40)
score = 0
high_score = 0
active_score = True


#-------------------------------------------------------------------------------------------------------------#
create_pipe = pygame.USEREVENT
creat_falp = pygame.USEREVENT +1
pygame.time.set_timer(creat_falp , 90)
pygame.time.set_timer(create_pipe , 1200)

#-----------------------------------------------------------------------------------------------------------#



win_sound = pygame.mixer.Sound('F:/flatybird/music/poan.wav')
game_over_sound = pygame.mixer.Sound('F:/flatybird/music/over.wav')

#-----------------------------------------------------------------------------------------------------#

background_imag = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/bg2.png'))
floor_image = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/floor.png'))
bird_image_down = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/bird_down.png'))
bird_image_mid = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/bird_mid.png'))
bird_image_up = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/bird_up.png'))
bird_list = [bird_image_down , bird_image_mid , bird_image_up]
bird_image = bird_list[bird_list_index]
pipe_image = pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/pipe_green.png'))
game_over_image =pygame.transform.scale2x(pygame.image.load('F:/flatybird/img/message.png'))
game_over_image_rect = game_over_image.get_rect(center=(288,512))


def generate_pipe_rect():
    random_pipe = random.randrange(400, 800)
    pipe_rect_top = pipe_image.get_rect(midbottom = (700, random_pipe - 300))
    pipe_rect_bottom = pipe_image.get_rect(midtop = (700, random_pipe))
    return pipe_rect_top,pipe_rect_bottom

def move_pipe_rect(pipes): 
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes

#This Def For Flip Top pipe
def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            main_screen.blit(pipe_image, pipe)
        else:
            reversed_pipes = pygame.transform.flip(pipe_image,False,True)
            main_screen.blit(reversed_pipes, pipe)
        main_screen.blit(pipe_image, pipe)


def check_collision(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
        if bird_image_rect.top <= -70 or bird_image_rect.bottom >= 800:
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
    return True


def bird_animion():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center = (100 , bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), False , (255,255,255))
        text1_rect = text1.get_rect(center =(300,170))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        #Score
        text1 = game_font.render(f'Score: {score}', False , (255,255,255))
        text1_rect = text1.get_rect(center =(300,170))
        main_screen.blit(text1, text1_rect)
        #Hight Score
        text2 = game_font.render(f'HighScore: {score}', False , (255,255,255))
        text2_rect = text2.get_rect(center =(300,650))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        high_score = score
    return high_score

#-----------------------------------------------------------------------------------------------------------#
bird_image_rect = bird_image.get_rect(center = (100, 520))

#Game Display
main_screen = pygame.display.set_mode((display_width , display_height))


#Game Timer
clock=pygame.time.Clock()

#Game Logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #End Pygame Modules
            pygame.quit()
            #Terminal Program
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movment = 0
                bird_movment -= 7
            if event.key == pygame.K_r and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (100 , 512)
                bird_movment = 0

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == creat_falp:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index =0
            
            bird_image, bird_image_rect = bird_animion()
            
    
    
    #Display BG2.png
    main_screen.blit(background_imag , (0, 0))

    if game_status:
        #Display bird image
        main_screen.blit(bird_image ,bird_image_rect)
        #Chech For Collision
        game_status = check_collision(pipe_list)
        #Move Pipe#
        pipe_list = move_pipe_rect (pipe_list)
        display_pipes(pipe_list)
        #Show Score
        update_score()
        display_score('active')
    else:
        main_screen.blit(game_over_image , game_over_image_rect)
        display_score('game_over')

    #Floor Gravity and bird Movment
    bird_movment += gravity
    bird_image_rect.centery += bird_movment
    #Display Floor.png
    main_screen.blit(floor_image ,(floor_x, 800))
    main_screen.blit(floor_image ,(floor_x + 576, 800))
    if floor_x <= -576:
        floor_x = 0
    floor_x -= 1
    pygame.display.update()
    #Set Game Speed
    clock.tick(88)#this number saying level hard or soft this game
