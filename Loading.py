import pygame
import config
from config import *

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")


## load images ########

tree = pygame.image.load("images/tree.png")
tree = pygame.transform.scale(tree, (250, 350))


grass = pygame.image.load("images/grass.png")
grass = pygame.transform.scale(grass, (900, 150))

# Set up colors
WHITE = (255, 255, 255)

# Game loop
running = True
while running:
    screen.fill(LIGHT_PURPLE)  # Fill screen with white
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(grass, (GRASS_LOC))
    screen.blit(tree, (50, 250))
    
    
    
    
    
    pygame.display.flip()  # Update display

# Quit Pygame
pygame.quit()
