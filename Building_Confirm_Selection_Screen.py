import pygame
import Building_Selection_Screen
import Building_Congratz_Screen

def runConfirmationScreen(imagepath):
    # Initialize pygame
    img_path = imagepath
    pygame.init()

    # Screen settings
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_COLOR = (58, 154, 12)
    SQUARE_SIZE = 200  # Large square for image
    RECT_WIDTH, RECT_HEIGHT = 400, 50  # Rectangle for confirmation text
    TITLE_SIZE = (400, 100)
    CIRCLE_RADIUS = 50

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Image Confirmation")

    background = pygame.image.load("assets/images/others/sky.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    title = pygame.image.load("images/buildingconfrim.png")
    title = pygame.transform.scale(title, TITLE_SIZE)

    # Calculate positions
    square_x = (SCREEN_WIDTH - SQUARE_SIZE) // 2
    square_y = (SCREEN_HEIGHT - SQUARE_SIZE) // 2
    rect_x = (SCREEN_WIDTH - RECT_WIDTH) // 2
    rect_y = square_y - RECT_HEIGHT - 20  # Place above the square with padding

    # Positions for circles
    circle_left_x = square_x - CIRCLE_RADIUS - 50
    circle_right_x = square_x + SQUARE_SIZE + 50 + CIRCLE_RADIUS
    circle_y = square_y + SQUARE_SIZE // 2

    # Load and resize image
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

    # Font settings
    font = pygame.font.Font(None, 36)
    yes_text = font.render("YES", True, (255, 255, 255))
    no_text = font.render("NO", True, (255, 255, 255))

    # Function to check if a point is inside a circle
    def is_inside_circle(point, circle_x, circle_y, radius):
        return (point[0] - circle_x) ** 2 + (point[1] - circle_y) ** 2 <= radius ** 2

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_inside_circle(mouse_pos, circle_left_x, circle_y, CIRCLE_RADIUS):
                    print("YES clicked! Proceeding with selection.")
                    Building_Congratz_Screen.runBuildingCongratz(img_path)
                elif is_inside_circle(mouse_pos, circle_right_x, circle_y, CIRCLE_RADIUS):
                    print("NO clicked! Cancelling selection.")  # Replace with actual logic
                    Building_Selection_Screen.runBuildingSelectionScreen()
                    running = False  # Close the confirmation screen

        screen.blit(background, (0, 0))
        
        # Draw image square
        screen.blit(image, (square_x, square_y))
        screen.blit(title, (square_x / 2 + 50, square_y - 150))
        
        # Draw YES and NO circles
        pygame.draw.circle(screen, (0, 255, 0), (circle_left_x, circle_y), CIRCLE_RADIUS)  # Green circle
        pygame.draw.circle(screen, (255, 0, 0), (circle_right_x, circle_y), CIRCLE_RADIUS)  # Red circle
        
        # Draw YES and NO text
        screen.blit(yes_text, (circle_left_x - yes_text.get_width() // 2, circle_y - yes_text.get_height() // 2))
        screen.blit(no_text, (circle_right_x - no_text.get_width() // 2, circle_y - no_text.get_height() // 2))
        
        pygame.display.flip()

    pygame.quit()


