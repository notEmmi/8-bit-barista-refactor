import pygame
import pygame_gui
import sqlite3
import bcrypt
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame GUI Registration")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

WHITE = (255, 255, 255)

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

def hash_password(password):
    """Encrypts password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def register_user():
    """Registers the user in the SQLite database."""
    global message_label
    username = username_input.get_text().strip()
    password = password_input.get_text().strip()

    if not username or not password:
        message_label.set_text("Please fill in both fields!")
        return

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        message_label.set_text("Username already taken!")
        return

    encrypted_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
    conn.commit()

    message_label.set_text(f"User '{username}' registered successfully!")
    username_input.set_text("")
    password_input.set_text("")

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
