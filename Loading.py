import pygame
import config
from config import *

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")

# Set up colors
WHITE = (255, 255, 255)

# Game loop
running = True
while running:
    screen.fill(LIGHT_PURPLE)  # Fill screen with white
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()  # Update display

# Quit Pygame
pygame.quit()
