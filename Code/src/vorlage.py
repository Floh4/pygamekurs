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
#   Hier kommt dann unser Code hin
print("Es funktioniert")
