import pygame
import random

# * import custom library
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from Custom_Library.pong_extension import (Player,
                                           Ball, 
                                           accelerate_ball, 
                                           keybind, 
                                           handle_exit)

# * initialize pygame
pygame.init()
pygame.font.init()
score_font = pygame.font.SysFont('Georgia', 14)
screen = pygame.display.set_mode((850, 500))
clock = pygame.time.Clock()

# ~     Hier kommt dann unser Code hin

# KONSTANTEN

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# SPIELER KONSTANTEN

PLAYER_WIDTH = 6
PLAYER_HEIGHT = 60

# Ball KONSTANTEN

BALL_RADIUS = 7
GESCHWINDIGKEITSGRENZE = 5
SPIELERGESCHWINDIGKEIT = 8
GESCHWINDIKGKEITSFAKTOR = 0

# initialize players and ball

player1 = Player((0, 220), (PLAYER_WIDTH, PLAYER_HEIGHT))
player2 = Player((SCREEN_WIDTH - PLAYER_WIDTH, 220), (PLAYER_WIDTH, PLAYER_HEIGHT))
ball = Ball(radius = BALL_RADIUS)

# Win Detection Variabeln

player1_score = 0
player2_score = 0

score_surface_1 = score_font.render(f"Score {player1_score}", True, (255, 255, 255))
score_surface_2 = score_font.render(f"Score {player2_score}", True, (255, 255, 255))

# start game funktion
def ball_start(ball_pong): # * gib ball random start richtung
    ball_pong.pos.x, ball_pong.pos.y = 425, 250
    random_number = random.randint(1, 4)
    match random_number:  
        case 1:
            ball_pong.velocity.x = 2
            ball_pong.velocity.y = 2.5
        case 2:
            ball_pong.velocity.x = -2
            ball_pong.velocity.y = 2.5
        case 3:
            ball_pong.velocity.x = 2
            ball_pong.velocity.y = -2.5
        case 4:
            ball_pong.velocity.x = -2
            ball_pong.velocity.y = -2.5

ball_start(ball)

while True: # main loop
    handle_exit()
    screen.fill((0, 0, 0))

    # Key input

    key = pygame.key.get_pressed()
    if key[pygame.K_q]:  # optional
        pygame.quit()
        sys.exit()
    keybind(pygame.K_w, pygame.K_s, player1, SPIELERGESCHWINDIGKEIT, SCREEN_HEIGHT, PLAYER_HEIGHT)
    keybind(pygame.K_UP, pygame.K_DOWN, player2, SPIELERGESCHWINDIGKEIT, SCREEN_HEIGHT, PLAYER_HEIGHT)

    # Ball Logik
    ## - Kollisionen mit der Wand (Dem Fenster) -

    if ((SCREEN_HEIGHT - BALL_RADIUS < ball.pos.y or 0 + BALL_RADIUS > ball.pos.y)):
        ball.velocity.y *= -1

    ## - Kollision mit player1 -

    if (pygame.Rect.colliderect(player1.rectangle, ball.hitbox)):
        diff_player_ball = (player1.middle_point - ball.pos.y)

        ball.velocity.x *= -1
        ball.move((((player1.left_top + PLAYER_WIDTH) - (ball.pos.x - BALL_RADIUS))), 0) 
        accelerate_ball(ball, diff_player_ball, GESCHWINDIGKEITSGRENZE)
    
    ## - Kollision mit player2 -

    if (pygame.Rect.colliderect(player2.rectangle, ball.hitbox)):
        diff_player_ball = (player2.middle_point - ball.pos.y)

        ball.velocity.x *= -1
        ball.move(((player2.left_top - (ball.pos.x + BALL_RADIUS))), 0)
        accelerate_ball(ball, diff_player_ball, GESCHWINDIGKEITSGRENZE)

    ## - Ball updaten -

    ball.move(ball.velocity.x, ball.velocity.y)
    ball.hitbox_follow()

    # WIN DETECTION *optional* 

    # if ((SCREEN_WIDTH + BALL_RADIUS) < ball.pos.x or 0 - BALL_RADIUS > ball.pos.x):
    if (SCREEN_WIDTH + BALL_RADIUS) < ball.pos.x:
        player1_score += 1
        score_surface_1 = score_font.render(f"Score {player1_score}", True, (255, 255, 255))
        ball_start(ball)

    elif (0 - BALL_RADIUS) > ball.pos.x:
        player2_score += 1
        score_surface_2 = score_font.render(f"Score {player2_score}", True, (255, 255, 255))
        ball_start(ball)

    # Score hinmalen

    screen.blit(score_surface_1, (20, 20))
    screen.blit(score_surface_2, (SCREEN_WIDTH - 20 - score_surface_2.get_width(), 20))
    
    # Spieler und Ball updaten und Zeichnen + Bildschirm updaten und fps zu 60

    player1.update(screen)                                                   
    player2.update(screen)
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)