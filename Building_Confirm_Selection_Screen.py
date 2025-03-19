import pygame


def runConfirmationScreen(imagepath):
# Initialize pygame
    img_path = imagepath
    pygame.init()

    # Screen settings
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_COLOR = (58, 154, 12)
    SQUARE_SIZE = 200  # Large square for image
    RECT_WIDTH, RECT_HEIGHT = 400, 50  # Rectangle for confirmation text

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Image Confirmation")

    background = pygame.image.load("assets/images/others/sky.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Calculate positions
    square_x = (SCREEN_WIDTH - SQUARE_SIZE) // 2
    square_y = (SCREEN_HEIGHT - SQUARE_SIZE) // 2
    rect_x = (SCREEN_WIDTH - RECT_WIDTH) // 2
    rect_y = square_y - RECT_HEIGHT - 20  # Place above the square with padding

    # Load and resize image (Replace with actual file path)
      # Change this to your image path
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

    # Font settings
    font = pygame.font.Font(None, 36)
    text = font.render("IS THIS THE HOME YOU WANT?", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, rect_y + RECT_HEIGHT // 2))

    # Main loop
    running = True
    while running:
        screen.fill(SCREEN_COLOR)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background,(0,0))
        
        # Draw confirmation text rectangle
        pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT))
        screen.blit(text, text_rect)
        
        # Draw image square
        # pygame.draw.rect(screen, (255, 255, 255), (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE), 2)  # White border
        screen.blit(image, (square_x, square_y))
        
        pygame.display.flip()

    pygame.quit()