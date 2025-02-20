import pygame
from pygame import mixer
from Music import Music

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login Screen")

# Colors ill use for bowxes 
WHITE = (255, 255, 255)
LIGHT_PURPLE = (200, 162, 200)
DARK_PURPLE = (150, 112, 150)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Fonts
font = pygame.font.Font(None, 36)

# Input box positions
title_box = pygame.Rect(200, 40, 200, 40)
title_box_background = pygame.image.load("images/woodPanel.png")
title_box_background = pygame.transform.scale(title_box_background, (200,40))

username_box = pygame.Rect(200, 100, 200, 40)
password_box = pygame.Rect(200, 160, 200, 40)
login_button = pygame.Rect(175, 230, 150, 50)

######################## BACKGROUND IMAGES ###################################


BACKGROUND=pygame.image.load("images/sky.png").convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

TREE_LEFT = pygame.image.load("images/tree.png")
TREE_LEFT = pygame.transform.scale(TREE_LEFT, (150,150))
                                               

# Input variables
username = ""
password = ""
active_box = None  # Track which box is active
password_hidden = True  # Hide password input


## PLAY LOG IN SCREEN TRACK #############

mixer.init()
mixer.music.load("Tracks/LogInTrack.mp3")
mixer.music.play()

running = True
while running:
    screen.fill(WHITE)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if username_box.collidepoint(event.pos):
                active_box = "username"
            elif password_box.collidepoint(event.pos):
                active_box = "password"
            elif login_button.collidepoint(event.pos):
                print(f"Logging in with:\nUsername: {username}\nPassword: {password}")
            
            ################ START OF LOGIN LOGIC WHEN I GET THERE #####################
            
            
            else:
                active_box = None

        elif event.type == pygame.KEYDOWN:
            if active_box == "username":
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    active_box = "password"  # Switch to password field
                else:
                    username += event.unicode

            elif active_box == "password":
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    print(f"Logging in with:\nUsername: {username}\nPassword: {password}")
                    # Add authentication logic here
                else:
                    password += event.unicode
    

    
    #DRAW BACKGROUND
    screen.blit(BACKGROUND, (0,0))
    screen.blit(TREE_LEFT, (0,250))

    # Draw input boxes
    pygame.draw.rect(screen, LIGHT_PURPLE, title_box, 2 )
    pygame.draw.rect(screen, LIGHT_PURPLE if active_box == "username" else GRAY, username_box, 2)
    pygame.draw.rect(screen, LIGHT_PURPLE if active_box == "password" else GRAY, password_box, 2)
    pygame.draw.rect(screen, DARK_PURPLE, login_button)

    # Render text labels
    title_text = font.render("8-BIT BARISTA", True, BLACK)
    username_text = font.render("Username:", True, BLACK)
    password_text = font.render("Password:", True, BLACK)
    screen.blit(username_text, (50, 110))
    screen.blit(password_text, (50, 170))
    screen.blit(title_box_background,(200,40))
    screen.blit(title_text,(212, 45))
    

    # Render user input
    username_surface = font.render(username, True, BLACK)
    screen.blit(username_surface, (username_box.x + 10, username_box.y + 10))

    # Mask password with asterisks
    password_display = "*" * len(password) if password_hidden else password
    password_surface = font.render(password_display, True, BLACK)
    screen.blit(password_surface, (password_box.x + 10, password_box.y + 10))

    # Draw login button text
    login_text = font.render("Log In", True, WHITE)
    screen.blit(login_text, (login_button.x + 40, login_button.y + 10))

    # Update display
    pygame.display.flip()

pygame.quit()