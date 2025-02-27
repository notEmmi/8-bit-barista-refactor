import pygame

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# Fonts
font = pygame.font.Font(pygame.font.match_font("courier"), 50)

# Back Button
back_button = pygame.Rect(320, 500, 160, 50)  # Centered back button

# Function to display the credits screen
def show_credits(screen, events):
    screen.fill(BLACK)

    # Draw "CREDITS" Title
    credits_text = font.render("CREDITS", True, WHITE)
    screen.blit(credits_text, (400 - credits_text.get_width() // 2, 250))

    # Draw Back Button
    pygame.draw.rect(screen, BROWN, back_button, border_radius=10)
    back_text = font.render("BACK", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

    # Handle Events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(pygame.mouse.get_pos()):
                return "menu"  # Correct way: return a value

    return "credits"  # Stay on credits screen