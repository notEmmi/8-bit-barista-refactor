import pygame
from pygame import mixer
from Music import Music
import sqlite3
import config
from config import *

## create a connection to my user databe aswell as a cursor to execture cmds
dbConnection = sqlite3.connect("mydatabase.db")
cursor = dbConnection.cursor()

def check_username(username):

    cursor.execute("SELECT COUNT(*) FROM users WHERE name = ?", (username,))  ## this is safeest way to prevent sql inejction
    count = cursor.fetchone()[0]  # Fetch the 2nd column of the first row that should have the useranmes
    return count > 0  # Return True if count > 0, else False

def check_password(password):

    cursor.execute("SELECT COUNT(*) FROM users WHERE password = ?", (password,))  ## this is safeest way to prevent sql inejction
    count = cursor.fetchone()[0]  # Fetch the 2nd column of the first row that should have the useranmes
    return count > 0  # Return True if count > 0, else False

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login Screen")

# Colors ill use for bowxes 


# Fonts
font = pygame.font.Font(None, 36)

# Input box positions



grass = pygame.image.load("images/grass.png")
grass = pygame.transform.scale(grass,(700, 75))

username_box = pygame.Rect(200, 100, 200, 40)
password_box = pygame.Rect(200, 160, 200, 40)
login_button = pygame.Rect(175, 230, 150, 50)

######################## BACKGROUND IMAGES ###################################


sky=pygame.image.load("images/sky.png").convert_alpha()
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))

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
                    userExists = check_username(username)
                    if userExists == 1:
                        print("username exists!")
                    elif userExists == 0:
                        print("invalid username!")
                    passwordExists = check_password(password)
                    if passwordExists == 1:
                        ## go to start screen
                        print("password exists")
                    elif passwordExists == 0:
                        print("invalid password!")
                            

                    
                else:
                    password += event.unicode
    

    
    #DRAW BACKGROUND
    screen.blit(sky, SKY_LOC)
    screen.blit(grass,GRASS_LOC)
    screen.blit(TREE_LEFT, (0,250))

    # Draw input boxes
   
    pygame.draw.rect(screen, LIGHT_PURPLE if active_box == "username" else GRAY, username_box, 2)
    pygame.draw.rect(screen, LIGHT_PURPLE if active_box == "password" else GRAY, password_box, 2)
    pygame.draw.rect(screen, DARK_PURPLE, login_button)

    # Render text labels
    title_text = pygame.image.load("images/title.png")
    title_text = pygame.transform.scale(title_text, (150,40))
    username_text = pygame.image.load("images/username.png")
    username_text = pygame.transform.scale(username_text, (150,40))
    password_text = pygame.image.load("images/password.png")
    password_text = pygame.transform.scale(password_text, (150,40))
    screen.blit(username_text, USERNAME_TEXT_LOC)
    screen.blit(password_text, PASSWORD_TEXT_LOC )
   
    screen.blit(title_text,TITLE_TEXT_LOC)
    
    

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