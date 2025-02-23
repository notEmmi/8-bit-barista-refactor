import pygame

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

rain = pygame.image.load("images/rain.png")
rain = pygame.transform.scale(rain, (WIDTH, HEIGHT))
# Error message
error_message = "An error has occurred. Press ENTER TO RETURN TO LOG-IN."

running = True
while running:
      # Set background to red
    
    # Render error message
    text_surface = font.render(error_message, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(rain, (0,0))
    screen.blit(text_surface, text_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit on ESC key
                running = False

    pygame.display.flip()  # Update the screen

pygame.quit()