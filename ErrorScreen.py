import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK =(0,0,0)
FONT_SIZE = 40

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Error Screen")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

darkbg = pygame.image.load("images/darkbg.png")
darkbg = pygame.transform.scale(darkbg, (WIDTH, HEIGHT))

errorsign = pygame.image.load("images/errorsign_transparent.png")
errorsign = pygame.transform.scale(errorsign, (250, 400))

cloud = pygame.image.load("images/rain_transparent.png")
cloud = pygame.transform.scale(cloud, (100, 100))


# Error message

mixer.init()
mixer.music.load("Tracks/8-bit-arcade-mode-158814.mp3")
mixer.music.play()


running = True
while running:
      # Set background to red
    
    # Render error message
   
    screen.blit(darkbg, (0,0))
    screen.blit(errorsign, ((WIDTH/2)-125,(HEIGHT/2)-100))
    screen.blit(cloud, (((WIDTH/2)-50),(HEIGHT/2)-250))
    screen.blit(cloud, (((WIDTH/2)-250),(HEIGHT/2)-250))
    screen.blit(cloud, (((WIDTH/2)+150),(HEIGHT/2)-250))


   

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit on ESC key
                running = False

    pygame.display.flip()  # Update the screen

pygame.quit()