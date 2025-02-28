import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Four Rectangles")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTBROWN = (254, 195, 117)
BACKGROUNDBROWN = (205,149,74)

# Rectangle dimensions
RECT_WIDTH, RECT_HEIGHT = 200, 100
SPACING = 20

# Calculate center positions
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Define rectangles
backgroundRect = pygame.Rect(0,0,WIDTH,HEIGHT)
rect1 = pygame.Rect(center_x - RECT_WIDTH - SPACING // 2, center_y - RECT_HEIGHT - SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
rect2 = pygame.Rect(center_x + SPACING // 2, center_y - RECT_HEIGHT - SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
rect3 = pygame.Rect(center_x - RECT_WIDTH - SPACING // 2, center_y + SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
rect4 = pygame.Rect(center_x + SPACING // 2, center_y + SPACING // 2, RECT_WIDTH, RECT_HEIGHT)

# Create surfaces for rectangles
backgroundRect_surface = pygame.Surface((WIDTH,HEIGHT))
backgroundRect_surface.fill(BACKGROUNDBROWN)
rect_surface1 = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
rect_surface1.fill(LIGHTBROWN)
rect_surface2 = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
rect_surface2.fill(LIGHTBROWN)
rect_surface3 = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
rect_surface3.fill(LIGHTBROWN)
rect_surface4 = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
rect_surface4.fill(LIGHTBROWN)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw rectangles using screen.blit
    screen.blit(backgroundRect_surface, backgroundRect.topleft)
    screen.blit(rect_surface1, rect1.topleft)
    screen.blit(rect_surface2, rect2.topleft)
    screen.blit(rect_surface3, rect3.topleft)
    screen.blit(rect_surface4, rect4.topleft)
    
    
    pygame.display.flip()

pygame.quit()
