import pygame
from pygame import mixer



def runSampleStartScreen():
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    RED = (200, 0, 0)
    WHITE = (255, 255, 255)
    BLACK =(0,0,0)
    FONT_SIZE = 25

    # Setup display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SAMPLE START SCREEN")
    clock = pygame.time.Clock()
    TIMER_CHANGE_SCREEN = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_CHANGE_SCREEN, 5000)

    # Load font
    font = pygame.font.Font(None, FONT_SIZE)
    textTitle = font.render("SUCCESFULLY SENT TO START SCREEN AFTER LOADING!", True, BLACK)
    rectTitle = textTitle.get_rect(center=screen.get_rect().center)




    sky = pygame.image.load("images/sky.png")
    sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))


    # Error message

    mixer.init()
    mixer.music.load("tracks/menu-music.mp3")
    mixer.music.play()


    running = True
    while running:
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close button
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit on ESC key
                    running = False
            


            screen.blit(sky, (0,0))
            screen.blit(textTitle, rectTitle)

            pygame.display.flip()  # Update the screen

    pygame.quit()