import pygame
from pygame import mixer
def runUnlock():
# Initialize pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("New Recipe Unlocked")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHTBROWN = (254, 195, 117)

    # Fonts
    font_large = pygame.font.Font(pygame.font.match_font("Irish Grover"), 36)
    font_small = pygame.font.Font(pygame.font.match_font("Irish Grover"), 24)

    # Text
    title_text1 = "CONGRATS!!!"
    title_text2 =  "YOU'VE UNLOCKED A NEW RECIPE!!!"
    title_surface1 = font_large.render(title_text1, True, BLACK)
    title_surface2 = font_small.render(title_text2, True, BLACK)

    background = pygame.image.load("images/pinksky.png")
    background = pygame.transform.scale(background,(WIDTH,HEIGHT))

    title_rect1 = title_surface1.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    title_rect2 = title_surface2.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Image placeholder (Centered square for future image)
    image_rect_size = 200
    image_rect = pygame.Rect(WIDTH // 2 - image_rect_size // 2, HEIGHT // 2, image_rect_size, image_rect_size)
    image_rect_surface = pygame.Surface((200,200))
    image_rect_surface.fill(LIGHTBROWN)

    muffin = pygame.image.load("images/muffin.png")
    muffin = pygame.transform.scale(muffin,image_rect.size)

    exclaimationPoint = pygame.image.load("images/exPoint.png")
    exclaimationPoint = pygame.transform.scale(exclaimationPoint,(8,8))
    mixer.init()
    mixer.music.load("tracks/06 - Victory!.mp3")
    mixer.music.play()
    # Main loop
    running = True
    while running:
        screen.fill(LIGHTBROWN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw title text
        screen.blit(background,(0,0))
        screen.blit(image_rect_surface, (WIDTH // 2 - image_rect_size // 2, HEIGHT // 2) )
        screen.blit(title_surface1, title_rect1.topleft)
        screen.blit(title_surface2, title_rect2.topleft)
        screen.blit(muffin,image_rect.topleft)
        
        # Draw placeholder for image
        pygame.draw.rect(screen, BLACK, image_rect, 3)  # Black border for visibility
        
        pygame.display.flip()

    pygame.quit()