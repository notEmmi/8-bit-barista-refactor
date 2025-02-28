import pygame

# Initialize pygame
def runPopular():

    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four Rectangles")

    kitchen =pygame.image.load("images/kitchen.png")
    kitchen =pygame.transform.scale(kitchen,(WIDTH, HEIGHT))


    # Colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    LIGHTBROWN = (254, 195, 117)
    BACKGROUNDBROWN = (205, 149, 74)
    SADDLEBROWN =(139, 69, 19)
    BLACK = (0, 0, 0)

    # Rectangle dimensions
    POPULAR_TEXT_WIDTH,POPULAR_TEXT_HEIGHT = 300, 100
    RECT_WIDTH, RECT_HEIGHT = 200, 100
    SPACING = 20

    # Calculate center positions
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Define rectangles
    popularTextRect = pygame.Rect(center_x-150, center_y - 225, POPULAR_TEXT_WIDTH,POPULAR_TEXT_HEIGHT )
    backgroundRect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    topLeftRect = pygame.Rect(center_x - RECT_WIDTH - SPACING // 2, center_y - RECT_HEIGHT - SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
    topRightRect = pygame.Rect(center_x + SPACING // 2, center_y - RECT_HEIGHT - SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
    bottomLeftRect = pygame.Rect(center_x - RECT_WIDTH - SPACING // 2, center_y + SPACING // 2, RECT_WIDTH, RECT_HEIGHT)
    bottomRightRect = pygame.Rect(center_x + SPACING // 2, center_y + SPACING // 2, RECT_WIDTH, RECT_HEIGHT)

    # Create surfaces for rectangles
    popularTextRect_surface = pygame.Surface((POPULAR_TEXT_WIDTH, POPULAR_TEXT_HEIGHT))
    popularTextRect_surface.fill(LIGHTBROWN)
    backgroundRect_surface = pygame.Surface((WIDTH, HEIGHT))
    backgroundRect_surface.fill(BACKGROUNDBROWN)
    topLeftRect_Surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
    topLeftRect_Surface.fill(LIGHTBROWN)
    topRightRect_Surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
    topRightRect_Surface.fill(LIGHTBROWN)
    bottomLeftRect_Surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
    bottomLeftRect_Surface.fill(LIGHTBROWN)
    bottomRightRect_Surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
    bottomRightRect_Surface.fill(LIGHTBROWN)



    # Load font
    font = pygame.font.Font(pygame.font.match_font("courier"), 24)
    popularFont = pygame.font.Font(pygame.font.match_font("courier"), 48)

    def draw_text(surface, text, rect, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect.topleft)

    # Main loop
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if topLeftRect.collidepoint(mouse_pos):
                topLeftRect_Surface.fill(SADDLEBROWN)
            
            elif topRightRect.collidepoint(mouse_pos):

                topRightRect_Surface.fill(SADDLEBROWN)

            elif bottomLeftRect.collidepoint(mouse_pos):

                bottomLeftRect_Surface.fill(SADDLEBROWN)
            

            elif bottomRightRect.collidepoint(mouse_pos):

                bottomRightRect_Surface.fill(SADDLEBROWN)



            
            
            
            else:
                topLeftRect_Surface.fill(LIGHTBROWN)
                topRightRect_Surface.fill(LIGHTBROWN)
                bottomLeftRect_Surface.fill(LIGHTBROWN)
                bottomRightRect_Surface.fill(LIGHTBROWN)


                
        
        # Draw rectangles using screen.blit
        screen.blit(kitchen, (0,0))
        screen.blit(popularTextRect_surface, popularTextRect.topleft)
        screen.blit(topLeftRect_Surface, topLeftRect.topleft)
        screen.blit(topRightRect_Surface, topRightRect.topleft)
        screen.blit(bottomLeftRect_Surface, bottomLeftRect.topleft)
        screen.blit(bottomRightRect_Surface, bottomRightRect.topleft)
        
        # Draw text centered in each rectangle
        draw_text(screen, "Popular", popularTextRect, popularFont, BLACK)

        
        
        pygame.display.flip()

    pygame.quit()
