import pygame
import sys
import os
#import character_selection

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-BIT BARISTA")

# Colors
LIGHT_BROWN = (99, 55, 44)  # Background
DARK_BROWN = (38, 35, 34)  # Inner background
BROWN = (99, 55, 44)  # Buttons and title bar
WHITE = (255, 255, 255)
SHADOW_COLOR = (20, 20, 20, 180)  # Shadow opacity adjustment

# Fonts
title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
button_font = pygame.font.Font(pygame.font.match_font('courier'), 22)

# Game States
MENU = "menu"
OPTIONS = "options"
CHARACTER_SELECTION = "character_selection"
CREDITS = "credits"
current_screen = MENU  # Start at the menu


def draw_blurred_shadow(surface, rect, blur_radius=10, offset_x=8, offset_y=8, border_radius=12):
    """Draws a smooth, blurred shadow for UI elements."""
    shadow_surface = pygame.Surface((rect.width + offset_x * 2, rect.height + offset_y * 2), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 0))  # Transparent layer
    shadow_rect = pygame.Rect(offset_x, offset_y, rect.width, rect.height)
    pygame.draw.rect(shadow_surface, SHADOW_COLOR, shadow_rect, border_radius=border_radius)
    surface.blit(shadow_surface, (rect.x, rect.y))


class Button:
    """UI Button with hover effects and shadows."""
    def __init__(self, text, x, y, width, height, action, border_radius=12):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BROWN
        self.border_radius = border_radius
        self.action = action  # Action defines which screen to switch to
    
    def draw(self, screen, mouse_pos):
        draw_blurred_shadow(screen, self.rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=self.border_radius)
        pygame.draw.rect(screen, DARK_BROWN if self.rect.collidepoint(mouse_pos) else BROWN, self.rect, border_radius=self.border_radius)
        text_surface = button_font.render(self.text, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


# Define Buttons
button_width, button_height = 200, 60
button_x = (WIDTH - button_width) // 2
button_spacing = 90
button_start_y = 220
buttons = [
    Button("START", button_x, button_start_y, button_width, button_height, CHARACTER_SELECTION),
    Button("OPTIONS", button_x, button_start_y + button_spacing, button_width, button_height, OPTIONS),
    Button("CREDITS", button_x, button_start_y + 2 * button_spacing, button_width, button_height, CREDITS),
    Button("EXIT", (WIDTH - 150) // 2, button_start_y + 3 * button_spacing, 150, 55, None)
]

# Load Coffee Cup Image
try:
    image_path = os.path.join("images", "coffee.png")
    coffee_img = pygame.image.load(image_path)

    coffee_img = pygame.transform.scale(coffee_img, (235,235))
except:
    coffee_img = None


# Function to draw the main menu
def show_menu():
    screen.fill(LIGHT_BROWN)

    # Inner Background
    center_rect = pygame.Rect(30, 20, WIDTH - 60, HEIGHT - 40)
    draw_blurred_shadow(screen, center_rect, blur_radius=15, offset_x=4, offset_y=4, border_radius=12)
    pygame.draw.rect(screen, DARK_BROWN, center_rect, border_radius=12)

    # Title Bar
    title_rect = pygame.Rect(160, 70, 480, 85)
    draw_blurred_shadow(screen, title_rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=12)
    pygame.draw.rect(screen, BROWN, title_rect, border_radius=12)
    screen.blit(title_font.render("8-BIT BARISTA", True, WHITE), title_font.render("8-BIT BARISTA", True, WHITE).get_rect(center=title_rect.center))

    # Mouse Tracking
    mouse_pos = pygame.mouse.get_pos()

    # Draw Buttons
    for button in buttons:
        button.draw(screen, mouse_pos)

    # Draw Coffee Cup
    if coffee_img:
      image_x = (WIDTH - coffee_img.get_width()) - 45
      image_y = (HEIGHT - coffee_img.get_height()) - 60
      screen.blit(coffee_img, (image_x, image_y))


# Main Loop
running = True
while running:
    events = pygame.event.get()
    screen.fill(LIGHT_BROWN)

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Handle screen transitions
    if current_screen == MENU:
        show_menu()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        if button.action:
                            current_screen = button.action
                        if button.text == "EXIT":
                            running = False
                        print(f"{button.text} button clicked!")

    #elif current_screen == CHARACTER_SELECTION:
        #current_screen = character_selection.show_character_selection(screen)
    elif current_screen == OPTIONS:
      import options  
      new_screen = options.show_options(screen, events)
      if new_screen == "menu":
          current_screen = MENU

    elif current_screen == CREDITS:
        import credits  
        new_screen = credits.show_credits(screen, events)  # Store return value      
        if new_screen == "menu":  # If "BACK" is clicked in credits.py
          current_screen = MENU  # Switch back to start menu

    pygame.display.flip()  # Update screen

pygame.quit()
sys.exit()