# import pygame
# import pygame_gui
# import sqlite3
# import bcrypt
# import sys
# import os

# class RegistrationApp:
#     def __init__(self):
#         pygame.init()
#         self.WIDTH, self.HEIGHT = 600, 400
#         self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         pygame.display.set_caption("Pygame GUI Registration")
#         self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
#         self.WHITE = (255, 255, 255)
#         self.conn = sqlite3.connect("mydatabase.db")
#         self.cursor = self.conn.cursor()
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL
#             )
#         """)
#         self.conn.commit()
#         self.setup_ui()
#         self.clock = pygame.time.Clock()
#         self.running = True

#     def setup_ui(self):
#         self.username_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 80), (100, 30)),
#                                                           text="Username:", manager=self.manager)
#         self.username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 80), (200, 30)),
#                                                                   manager=self.manager)
#         self.password_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 130), (100, 30)),
#                                                           text="Password:", manager=self.manager)
#         self.password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 130), (200, 30)),
#                                                                   manager=self.manager)
#         self.register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 180), (100, 40)),
#                                                             text="Register", manager=self.manager)
#         self.message_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 240), (300, 30)),
#                                                          text="", manager=self.manager)

#     def hash_password(self, password):
#         """Encrypts password using bcrypt."""
#         salt = bcrypt.gensalt()
#         return bcrypt.hashpw(password.encode(), salt)

#     def register_user(self):
#         """Registers the user in the SQLite database."""
#         username = self.username_input.get_text().strip()
#         password = self.password_input.get_text().strip()

#         if not username or not password:
#             self.message_label.set_text("Please fill in both fields!")
#             return

#         self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#         if self.cursor.fetchone():
#             self.message_label.set_text("Username already taken!")
#             return

#         encrypted_password = self.hash_password(password)
#         self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
#         self.conn.commit()
#         self.message_label.set_text(f"User '{username}' registered successfully!")
#         self.username_input.set_text("")
#         self.password_input.set_text("")

#     def run(self):
#         while self.running:
#             time_delta = self.clock.tick(30) / 1000.0
#             self.screen.fill(self.WHITE)

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#                 if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.register_button:
#                     self.register_user()

#                 self.manager.process_events(event)

#             self.manager.update(time_delta)
#             self.manager.draw_ui(self.screen)
#             pygame.display.flip()

#         self.conn.close()
#         pygame.quit()
#         sys.exit()

# # Example usage
# # registration_app = RegistrationApp()
# # registration_app.run()

import pygame
import pygame_gui
import sqlite3
import bcrypt
import sys
import subprocess

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame GUI Registration")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
WHITE = (255, 255, 255)

# Connect to the same database as login
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# Ensure the users table exists and matches login structure
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

def hash_password(password):
    """Encrypts the password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def register_user():
    """Registers a new user in the database and redirects to login."""
    username = username_input.get_text().strip()
    password = password_input.get_text().strip()

    if not username or not password:
        message_label.set_text("Please fill in both fields!")
        return

    try:
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            message_label.set_text("Username already taken!")
            return

        encrypted_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
        conn.commit()

        message_label.set_text(f"User '{username}' registered successfully!")
        pygame.time.delay(1000)

        pygame.quit()
        conn.close()
        subprocess.run(["python", "Game.py"])
        sys.exit()
    
    except sqlite3.OperationalError as e:
        message_label.set_text(f"Database error: {e}")

<<<<<<< HEAD

registration_app = RegistrationApp()
registration_app.run()
=======
# UI Elements
username_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 80), (100, 30)),
                                             text="Username:", manager=manager)
username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 80), (200, 30)),
                                                     manager=manager)
password_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 130), (100, 30)),
                                             text="Password:", manager=manager)
password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 130), (200, 30)),
                                                     manager=manager)
register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 180), (100, 40)),
                                               text="Register", manager=manager)
message_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 240), (300, 30)),
                                            text="", manager=manager)

clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(30) / 1000.0
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == register_button:
            register_user()
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

conn.close()
pygame.quit()
sys.exit()
>>>>>>> ac7af8f32c89127a911bb6b11a9d1f30fb3e51ac
