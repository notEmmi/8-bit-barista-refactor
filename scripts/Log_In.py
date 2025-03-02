import pygame
from pygame import mixer
from Music import Music
import sqlite3
import config_logIn as config_logIn
from config_logIn import *
import bcrypt
import os
from Loading import LoadingScreen
from start_menu import StartMenu

class LogInScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.WIDTH, self.HEIGHT = 500, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Login Screen")

        # Colors
        # ...existing code...

        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Input box positions
        # ...existing code...

        self.grass = pygame.image.load(os.path.join("assets", "images", "others", "grass.png"))
        self.grass = pygame.transform.scale(self.grass, (700, 75))

        self.username_box = pygame.Rect(200, 100, 200, 40)
        self.password_box = pygame.Rect(200, 160, 200, 40)
        self.login_button = pygame.Rect(175, 230, 150, 50)

        # Background images
        self.sky = pygame.image.load(os.path.join("assets", "images", "others", "sky.png")).convert_alpha()
        self.sky = pygame.transform.scale(self.sky, (self.WIDTH, self.HEIGHT))

        self.TREE_LEFT = pygame.image.load(os.path.join("assets", "images", "others", "tree.png"))
        self.TREE_LEFT = pygame.transform.scale(self.TREE_LEFT, (150, 150))

        # Input variables
        self.username = ""
        self.password = ""
        self.active_box = None  # Track which box is active
        self.password_hidden = True  # Hide password input

        # Initialize database connection
        self.dbConnection = sqlite3.connect(os.path.join("assets", "database", "mydatabase.db"))
        self.cursor = self.dbConnection.cursor()

        # Play login screen track
        mixer.init()
        mixer.music.load(os.path.join("assets", "sounds", "LogInTrack.mp3"))
        mixer.music.set_volume(0.1) # Set volume to 10%
        mixer.music.play()

    def check_username(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def check_password(self, entered_password, stored_hash):
        """Checks if entered password matches the stored hash."""
        return bcrypt.checkpw(entered_password.encode(), stored_hash)

    def authenticate_user(self):
        userExists = self.check_username(self.username)
        if userExists:
            print("username exists!")
            self.cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
            result = self.cursor.fetchone()
            print("encrypted password", result)

            if result:
                stored_hash = result[0]
                if self.check_password(self.password, stored_hash):
                    print("Login successful!")
                    start_menu = StartMenu()
                    loading_screen = LoadingScreen(start_menu.run)
                    loading_screen.run()
                    print("password exists")
                else:
                    ErrorScreen.runError()
                    return False
            else:
                print("invalid username!")
                return False
        else:
            print("invalid username!")
            return False
        return True

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)  # Background color

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_box.collidepoint(event.pos):
                        self.active_box = "username"
                    elif self.password_box.collidepoint(event.pos):
                        self.active_box = "password"
                    elif self.login_button.collidepoint(event.pos):
                        print(f"Logging in with:\nUsername: {self.username}\nPassword: {self.password}")
                        if not self.authenticate_user():
                            running = False

                elif event.type == pygame.KEYDOWN:
                    if self.active_box == "username":
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.active_box = "password"
                        else:
                            self.username += event.unicode

                    elif self.active_box == "password":
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        elif event.key == pygame.K_RETURN:
                            print(f"Logging in with:\nUsername: {self.username}\nPassword: {self.password}")
                            if not self.authenticate_user():
                                running = False
                        else:
                            self.password += event.unicode

            # Draw background
            self.screen.blit(self.sky, SKY_LOC)
            self.screen.blit(self.grass, GRASS_LOC_LOGIN)
            self.screen.blit(self.TREE_LEFT, (0, 250))

            # Draw input boxes
            pygame.draw.rect(self.screen, LIGHT_PURPLE if self.active_box == "username" else GRAY, self.username_box, 2)
            pygame.draw.rect(self.screen, LIGHT_PURPLE if self.active_box == "password" else GRAY, self.password_box, 2)
            pygame.draw.rect(self.screen, DARK_PURPLE, self.login_button)

            # Render text labels
            title_text = pygame.image.load(os.path.join("assets", "images", "others", "title.png"))
            title_text = pygame.transform.scale(title_text, (150, 40))
            username_text = pygame.image.load(os.path.join("assets", "images", "others", "username.png"))
            username_text = pygame.transform.scale(username_text, (150, 40))
            password_text = pygame.image.load(os.path.join("assets", "images", "others", "password.png"))
            password_text = pygame.transform.scale(password_text, (150, 40))
            self.screen.blit(username_text, USERNAME_TEXT_LOC)
            self.screen.blit(password_text, PASSWORD_TEXT_LOC)
            self.screen.blit(title_text, TITLE_TEXT_LOC)

            # Render user input
            username_surface = self.font.render(self.username, True, BLACK)
            self.screen.blit(username_surface, (self.username_box.x + 10, self.username_box.y + 10))

            # Mask password with asterisks
            password_display = "*" * len(self.password) if self.password_hidden else self.password
            password_surface = self.font.render(password_display, True, BLACK)
            self.screen.blit(password_surface, (self.password_box.x + 10, self.password_box.y + 10))

            # Draw login button text
            login_text = self.font.render("Log In", True, WHITE)
            self.screen.blit(login_text, (self.login_button.x + 40, self.login_button.y + 10))

            # Update display
            pygame.display.flip()

        pygame.quit()

class ErrorScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.RED = (200, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 40

        # Setup display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Error Screen")
        self.clock = pygame.time.Clock()
        self.TIMER_CHANGE_SCREEN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMER_CHANGE_SCREEN, 5000)

        # Load font
        self.font = pygame.font.Font(None, self.FONT_SIZE)

        self.darkbg = pygame.image.load("assets/images/others/darkbg.png")
        self.darkbg = pygame.transform.scale(self.darkbg, (self.WIDTH, self.HEIGHT))

        self.errorsign = pygame.image.load("assets/images/others/errorsign_transparent.png")
        self.errorsign = pygame.transform.scale(self.errorsign, (250, 400))

        self.cloud = pygame.image.load("assets/images/others/rain_transparent.png")
        self.cloud = pygame.transform.scale(self.cloud, (100, 100))

        # Error message
        mixer.init()
        mixer.music.load("assets/sounds/error.mp3")
        mixer.music.play()

    def run(self):
        running = True
        while running:
            # Set background to red
            # Render error message
            self.screen.blit(self.darkbg, (0, 0))
            self.screen.blit(self.errorsign, ((self.WIDTH / 2) - 125, (self.HEIGHT / 2) - 100))
            self.screen.blit(self.cloud, (((self.WIDTH / 2) - 50), (self.HEIGHT / 2) - 250))
            self.screen.blit(self.cloud, (((self.WIDTH / 2) - 250), (self.HEIGHT / 2) - 250))
            self.screen.blit(self.cloud, (((self.WIDTH / 2) + 150), (self.HEIGHT / 2) - 250))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close button
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Exit on ESC key
                        running = False
                    elif event.key == pygame.K_RETURN:
                        # Call function from Log_In.py
                        log_in_screen = LogInScreen()
                        log_in_screen.run()
                        running = False

            self.clock.tick(30)
            pygame.display.flip()  # Update the screen

        pygame.quit()

if __name__ == "__main__":
    login_screen = LogInScreen()
    login_screen.run()