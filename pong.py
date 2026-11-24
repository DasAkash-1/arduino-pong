import pygame, sys
import os
import random
from menu import menu
import serial
import controls

pygame.init()

BASE = os.path.dirname(os.path.abspath(__file__))

SENSOR = True

WIDTH = 900
HEIGHT = 600

FONT = pygame.font.Font(os.path.join(BASE, "assets", "font", "PressStart2P-Regular.ttf"), 20)

BG = "#0f0526"
LINE_COLOR = "gray30"    
P1_COLOR = "yellow" 
P2_COLOR = "crimson"
BALL_COLOR = "coral"

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG!!!")
CLOCK = pygame.time.Clock()


# sounds
hit_sound = pygame.mixer.Sound(os.path.join(BASE, "assets", "audio", "hit.wav"))
wall_sound = pygame.mixer.Sound(os.path.join(BASE, "assets", "audio", "wall.wav"))
hit_sound.set_volume(0.4)
wall_sound.set_volume(0.4)


# player
player1 = pygame.Rect(90, HEIGHT / 2 - 50, 10, 100)
player2 = pygame.Rect(WIDTH - 90, HEIGHT / 2 - 50, 10, 100)

player1_score, player2_score = 0, 0


# ball
ball = pygame.Rect(WIDTH / 2 - 15,  HEIGHT / 2 - 15, 30, 30)
x_speed, y_speed = 1, 1

# menu
menu(SCREEN, CLOCK, FONT, BG, BALL_COLOR, P1_COLOR, P2_COLOR)

if SENSOR:
    controls.ser.reset_input_buffer()

while True:

    keys_pressed = pygame.key.get_pressed() 

    if SENSOR:
        controls.update()
        print(controls.disL, controls.disR)

        target1 = (controls.disL - controls.mn) / (controls.mx - controls.mn) * (HEIGHT - player1.height)
        target2 = (controls.disR - controls.mn) / (controls.mx - controls.mn) * (HEIGHT - player2.height)

        player1.top += (target1 - player1.top) * 0.2   # 0.2 smooth
        player2.top += (target2 - player2.top) * 0.2

    else:
        if keys_pressed[pygame.K_w]:
            if player1.top > 0: player1.top -= 3 # paddle speed 3 bhala in 120 ticks
        if keys_pressed[pygame.K_s]:
            if player1.bottom < HEIGHT: player1.bottom += 3


        if keys_pressed[pygame.K_UP]:
            if player2.top > 0: player2.top -= 3
        if keys_pressed[pygame.K_DOWN]:
            if player2.bottom < HEIGHT: player2.bottom += 3



    # ball boundary
    if ball.bottom >= HEIGHT: 
        y_speed = -1 # baire jaito na
    if ball.top <= 0: 
        y_speed = 1

    if ball.left <= 0:      # two R er point
        player2_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        wall_sound.play()

    if ball.right >= WIDTH: # one L er point
        player1_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        wall_sound.play()
    


    # hit logic
    if ball.colliderect(player1): 
        x_speed = 1
        hit_sound.play()
    if ball.colliderect(player2): 
        x_speed = -1
        hit_sound.play()

    

    ball.x += x_speed * 3
    ball.y += y_speed * 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu(SCREEN, CLOCK, FONT, BG, BALL_COLOR, P1_COLOR, P2_COLOR)
            player1_score, player2_score = 0, 0
            ball.center = (WIDTH / 2, HEIGHT / 2)

    # score
    score_text1 = FONT.render(f"Left: {player1_score}", True, "white")
    score_text2 = FONT.render(f"Right: {player2_score}", True, "white")

    


    SCREEN.fill(BG)



    # majher dotted line divde
    for i in range(0, HEIGHT, 30):
        pygame.draw.rect(SCREEN, "gray30", (WIDTH / 2 - 2, i, 4, 15), border_radius= 2)


    pygame.draw.circle(SCREEN, BALL_COLOR, ball.center, 15)
    pygame.draw.rect(SCREEN, P1_COLOR, player1, border_radius= 5)
    pygame.draw.rect(SCREEN, P2_COLOR, player2, border_radius= 5)


    SCREEN.blit(score_text1, (10, 10))
    SCREEN.blit(score_text2, (WIDTH - score_text2.get_width() - 10, 10))

        # charpashe white border, shobar upore draw hobe
    pygame.draw.rect(SCREEN, "white", SCREEN.get_rect(), 4)

    pygame.display.update()
    CLOCK.tick(60)