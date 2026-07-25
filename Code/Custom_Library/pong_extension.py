import pygame
import sys

pygame.init()
pygame.display.set_caption("Pong")

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def get_as_list(self):
        return (self.x, self.y)

class Player:
    def __init__(self, pos = (10, 10), size = (10, 10)):
        self.pos = Vector(pos[0], pos[1])
        self.size = list(size)
        self.rectangle = pygame.Rect(self.pos.get_as_list(), self.size)
        self.middle_point = (self.pos.y + (self.size[1] / 2))          # Für abprall in verschiedene Richtungen
        self.left_top = self.pos.x 

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rectangle)
    
    def move(self, relative_y):
        self.pos.y -= relative_y 
    
    def update(self, screen):                                                   # update player
        self.rectangle = pygame.Rect(self.pos.get_as_list(), self.size)   # K - Optimieren das nur updaten wenn er sich bewegt (optional)
        self.middle_point = (self.pos.y + (self.size[1] / 2))
        self.draw(screen)

class Ball:
    def __init__(self, pos = (425, 250), velocity = (0, 0), radius = 7):
        self.pos = Vector(pos[0], pos[1])
        self.velocity = Vector(velocity[0], velocity[1])
        self.radius = radius
        self.hitbox = pygame.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.pos.get_as_list(), self.radius)
    
    def move(self, relative_x, relative_y):
        self.pos.x += relative_x
        self.pos.y += relative_y

    def hitbox_follow(self):
        self.hitbox.center = (self.pos.x, self.pos.y)
    
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, "red", self.hitbox, 1) # * Nur zum debuggen

def accelerate_ball(ball_pong, diff_player_ball, geschwindigkeitsgrenze): # * Beschleunigt Ball
    if ((abs(ball_pong.velocity.x) < geschwindigkeitsgrenze and abs(ball_pong.velocity.y) < geschwindigkeitsgrenze) and abs(diff_player_ball) > 20 ): # * Nur wenn der Ball an den äußeren Enden vom Spieler trift, prallt der Ball in einem Winkel ab (Optional)
        if ball_pong.velocity.x > 0:
            ball_pong.velocity.x += 2
        else:
            ball_pong.velocity.x -= 2
        ball_pong.velocity.y += 0.1 * ((diff_player_ball - 10) * -0.1)  # * Wirkungsgrad wie stark es wirken soll
    elif (ball_pong.velocity.x < geschwindigkeitsgrenze and ball_pong.velocity.y < geschwindigkeitsgrenze):
        if ball_pong.velocity.x > 0:
            ball_pong.velocity.x += 2
        else:
            ball_pong.velocity.x -= 2
        ball_pong.velocity.y += 0.1

def keybind(key, key_pygame_up, key_pygame_down, player, spielergeschwindigkeit, screen_height, player_height): 
    if key[key_pygame_up] and player.pos.y > 0: # * damit der ball an der decke nicht runter geht
        player.move(spielergeschwindigkeit)
    if key[key_pygame_down] and player.pos.y < screen_height - player_height: # * damit der ball an dem boden nicht runter geht
        player.move(-spielergeschwindigkeit)

def handle_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
