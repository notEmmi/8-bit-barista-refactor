import pygame
from pygame import mixer
from first_page import Game

def runBuildingCongratz(imagepath):
    img_path = imagepath
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Start Adventure")

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BUTTON_COLOR = (245, 173, 66)
    BUTTON_HOVER = (255, 193, 86)
    BANNER_COLOR = (255, 226, 179)

    # Fonts
    font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 32)
    banner_font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 36)

    # Load background and house image
    background = pygame.image.load("images/pinksky.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    building = pygame.image.load(img_path).convert_alpha()
    building_rect_size = 200
    building = pygame.transform.scale(building, (building_rect_size, building_rect_size))
    building_rect = building.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    # Button
    button_text = "Start Your Adventure"
    button_surface = font.render(button_text, True, BLACK)
    button_width = button_surface.get_width() + 40
    button_height = button_surface.get_height() + 20
    button_rect = pygame.Rect(
        WIDTH // 2 - button_width // 2,
        HEIGHT // 2 + 100,
        button_width,
        button_height
    )

    # Banner
    banner_height = 60
    banner_rect = pygame.Rect(0, 0, WIDTH, banner_height)
    banner_text = "ENJOY YOUR NEW HOME!"
    banner_surface = banner_font.render(banner_text, True, BLACK)
    banner_text_rect = banner_surface.get_rect(center=(WIDTH // 2, banner_height // 2))

    # Music
    mixer.init()
    mixer.music.load("tracks/06 - Victory!.mp3")
    mixer.music.play()

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(building, building_rect.topleft)

        # Draw banner
        pygame.draw.rect(screen, BANNER_COLOR, banner_rect)
        screen.blit(banner_surface, banner_text_rect)

        # Button hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = button_rect.collidepoint(mouse_pos)
        button_color = BUTTON_HOVER if is_hovering else BUTTON_COLOR

        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        screen.blit(button_surface, (button_rect.centerx - button_surface.get_width() // 2,
                                     button_rect.centery - button_surface.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    from pet_selector import PetSelector
                    choose_pet = PetSelector(img_path)
                    choose_pet.run()
                    running = False

            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:
            #         game = Game(img_path)
            #         game.run()
            #         running = False

        pygame.display.flip()

    pygame.quit()
