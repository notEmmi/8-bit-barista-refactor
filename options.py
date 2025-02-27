import pygame
import sys
import controls  # Import Controls Page
import advanced  # Import Advanced Page
import start_menu  # Import Start Menu Page

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OPTIONS MENU")

# Colors
LIGHT_BROWN = (99, 55, 44)  # Outer Background
DARK_BROWN = (38, 35, 34)  # Middle Dark Background
BROWN = (99, 55, 44)  # Inner Panel Color
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
ACTIVE_COLOR = (160, 100, 80)

# Fonts
title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
button_font = pygame.font.Font(pygame.font.match_font('courier'), 18)
texture_font = pygame.font.Font(pygame.font.match_font('courier'), 22)

# Game State
MENU = "menu"
CONTROLS = "controls"
ADVANCED = "advanced"
BACK = "back"
EXIT = "exit"
current_screen = MENU  # Start on the menu

# Sliders (Volume Controls)
sliders = {
    "Master Volume": 0.5,
    "Music": 0.5,
    "SFX": 0.5
}
slider_rects = {}
active_slider = None

# Texture Settings
textures = ["Low", "Med", "High"]
texture_rects = []  # Stores hitboxes for texture buttons
selected_texture = "High"

# Buttons
buttons = {
    "CONTROLS": pygame.Rect(250, 420, 100, 35),
    "ADVANCED": pygame.Rect(460, 420, 100, 35),
    "BACK": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw sliders with `+` and `-` buttons
def draw_slider(name, y_pos, value):
    min_x, max_x = 280, 520
    slider_rect = pygame.Rect(min_x, y_pos, max_x - min_x, 5)
    handle_x = min_x + int(value * (max_x - min_x))
    slider_rects[name] = (min_x, max_x, y_pos)

    pygame.draw.rect(screen, WHITE, slider_rect)
    pygame.draw.circle(screen, (201, 125, 96), (handle_x, y_pos + 3), 8)
    text = button_font.render(name, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos - 25))

    # Draw `-` and `+` buttons
    pygame.draw.rect(screen, (201, 125, 96), pygame.Rect(min_x - 31, y_pos - 6, 18, 18), border_radius=3)
    pygame.draw.rect(screen, (201, 125, 96), pygame.Rect(max_x + 17, y_pos - 6, 18, 18), border_radius=3)
    minus_text = button_font.render("-", True, WHITE)
    plus_text = button_font.render("+", True, WHITE)
    screen.blit(minus_text, minus_text.get_rect(center=(min_x - 22, y_pos + 3)))
    screen.blit(plus_text, plus_text.get_rect(center=(max_x + 26, y_pos + 3)))

# Function to draw texture options
def draw_textures():
    global texture_rects
    texture_rects.clear()
    x_positions = [280, 400, 520]
    for i, texture in enumerate(textures):
        texture_rect = pygame.Rect(x_positions[i] - 9, 380, 17, 17)
        texture_rects.append(texture_rect)
        color = ACTIVE_COLOR if texture == selected_texture else GRAY
        pygame.draw.circle(screen, color, (x_positions[i], 385), 8)
        text = pygame.font.Font(pygame.font.match_font('courier'), 16).render(texture, True, WHITE)
        screen.blit(text, (x_positions[i] - text.get_width() // 2, 354))

# Function to show the options menu
def show_options(events):
    global current_screen, active_slider, selected_texture

    screen.fill(LIGHT_BROWN)

    # Draw Background Panels
    middle_rect = pygame.Rect(30, 20, WIDTH - 60, HEIGHT - 40)
    pygame.draw.rect(screen, DARK_BROWN, middle_rect, border_radius=12)
    panel_rect = pygame.Rect(180, 50, 450, 500)
    pygame.draw.rect(screen, BROWN, panel_rect, border_radius=12)

    # Draw Title
    title_text = title_font.render("OPTIONS", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 85))

    # Draw Sliders
    y_offset = 180
    for name, value in sliders.items():
        draw_slider(name, y_offset, value)
        y_offset += 50

    # Draw Texture Selection
    texture_text = texture_font.render("TEXTURES", True, WHITE)
    screen.blit(texture_text, (WIDTH // 2 - texture_text.get_width() // 2, 310))
    draw_textures()

    # Draw Buttons
    mouse_pos = pygame.mouse.get_pos()
    for name, rect in buttons.items():
        pygame.draw.rect(screen, (201, 125, 96), rect, border_radius=14)
        text = button_font.render(name, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    # Handle Events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check Buttons
            for name, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    if name == "CONTROLS":
                        current_screen = CONTROLS
                    elif name == "ADVANCED":
                        current_screen = ADVANCED
                    elif name == "BACK":
                        current_screen = BACK  # Back to Start Menu
                    print(f"{name} button clicked!")

            # Check Sliders (`+` and `-` buttons)
            for name, (min_x, max_x, y_pos) in slider_rects.items():
                if min_x - 30 < mouse_pos[0] < min_x - 10 and y_pos - 8 < mouse_pos[1] < y_pos + 12:
                    sliders[name] = max(0, sliders[name] - 0.1)
                elif max_x + 10 < mouse_pos[0] < max_x + 30 and y_pos - 8 < mouse_pos[1] < y_pos + 12:
                    sliders[name] = min(1, sliders[name] + 0.1)
                else:
                    handle_x = min_x + int(sliders[name] * (max_x - min_x))
                    if handle_x - 10 < mouse_pos[0] < handle_x + 10 and y_pos - 10 < mouse_pos[1] < y_pos + 10:
                        active_slider = name

            # Texture Selection (`Low, Med, High`)
            for i, texture_rect in enumerate(texture_rects):
                if texture_rect.collidepoint(mouse_pos):
                    selected_texture = textures[i]

        elif event.type == pygame.MOUSEBUTTONUP:
            active_slider = None

        elif event.type == pygame.MOUSEMOTION and active_slider:
            min_x, max_x, y_pos = slider_rects[active_slider]
            sliders[active_slider] = max(0, min(1, (mouse_pos[0] - min_x) / (max_x - min_x)))

    return current_screen

# Main Loop with Seamless Page Transitions
running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_screen == MENU:
        current_screen = show_options(events)
    elif current_screen == CONTROLS:
        current_screen = controls.show_controls(screen)
    elif current_screen == ADVANCED:
        current_screen = advanced.show_advanced(screen)
    elif current_screen == BACK:
        current_screen = start_menu.show_start_menu(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
