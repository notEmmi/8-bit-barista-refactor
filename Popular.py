import pygame
import Unlock
import settingsdata
from pygame import mixer

# Initialize pygame
def runPopular():

    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Popular")

    kitchen =pygame.image.load("images/kitchen.png")
    kitchen =pygame.transform.scale(kitchen,(WIDTH, HEIGHT))

    bagel =pygame.image.load("images/bagel.png")
    bagel =pygame.transform.scale(bagel,(RECT_WIDTH/2, RECT_HEIGHT/2))

    coffee =pygame.image.load("images/coffee.png")
    coffee =pygame.transform.scale(coffee,(RECT_WIDTH/2, RECT_HEIGHT/2))

    croisant =pygame.image.load("images/croisant.png")
    croisant =pygame.transform.scale(croisant,(RECT_WIDTH/2, RECT_HEIGHT/2))

    lock =pygame.image.load("images/lock.png")
    lock =pygame.transform.scale(lock,(RECT_WIDTH/2, RECT_HEIGHT/2))

    exclaimationPoint = pygame.image.load("images/exPoint.png")
    exclaimationPoint = pygame.transform.scale(exclaimationPoint,(30,30))

    popup = pygame.image.load("images/popup.png")
    popup = pygame.transform.scale(popup,(75,75))


    

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

    ## positions of images relative to the rectangles there drawn in ##############
    bagel_x = topLeftRect.x + (topLeftRect.width - bagel.get_width()) // 2
    bagel_y = topLeftRect.y + (topLeftRect.height - bagel.get_height()) // 2

    coffee_x = topRightRect.x + (topRightRect.width - coffee.get_width()) // 2
    coffee_y = topRightRect.y + (topRightRect.height - coffee.get_height()) // 2

    croisant_x = bottomLeftRect.x + (bottomLeftRect.width - croisant.get_width()) // 2
    croisant_y = bottomLeftRect.y + (bottomLeftRect.height - croisant.get_height()) // 2

    lock_x = bottomRightRect.x + (bottomRightRect.width - lock.get_width()) // 2
    lock_y = bottomRightRect.y + (bottomRightRect.height - lock.get_height()) // 2



    # Load font
    font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 24)
    popularFont = pygame.font.Font(pygame.font.match_font("Irish Grover"), 48)
    mixer.init()
    mixer.music.load("tracks/08 - Shop.mp3")
    mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
    mixer.music.play()
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

                bottomRightRect_Surface.fill(BLUE)

                ### logic for pop up bubble here

                




            
            
            
            else:
                topLeftRect_Surface.fill(LIGHTBROWN)
                topRightRect_Surface.fill(LIGHTBROWN)
                bottomLeftRect_Surface.fill(LIGHTBROWN)
                bottomRightRect_Surface.fill(LIGHTBROWN)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if bottomRightRect.collidepoint(event.pos):   ### if the position of the mousedown event is in the top left rectange postiton.. 
                 Unlock.runUnlock()
                 running = False


                
        
        # Draw rectangles using screen.blit
        screen.blit(kitchen, (0,0))
        screen.blit(popularTextRect_surface, popularTextRect.topleft)
        
        screen.blit(topLeftRect_Surface, topLeftRect.topleft)
        screen.blit(bagel, (bagel_x, bagel_y))
        screen.blit(topRightRect_Surface, topRightRect.topleft)
        screen.blit(coffee, (coffee_x, coffee_y))
        screen.blit(bottomLeftRect_Surface, bottomLeftRect.topleft)
        screen.blit(croisant, (croisant_x, croisant_y))
        screen.blit(bottomRightRect_Surface, bottomRightRect.topleft)
        screen.blit(lock, (lock_x, lock_y))
        mouse_pos = pygame.mouse.get_pos()
        if bottomRightRect.collidepoint(mouse_pos):
         screen.blit(popup,(425,250))
        
        # Draw text centered in each rectangle
        draw_text(screen, "Popular", popularTextRect, popularFont, BLACK)
        ##pygame.draw.circle(screen, WHITE, (bottomRightRect.topleft), 16)

        screen.blit(exclaimationPoint, (bottomRightRect.topleft))

        ##center_x - RECT_WIDTH - SPACING // 2
        
        pygame.display.flip()

    pygame.quit()
