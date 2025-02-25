import pygame
import sys
from loading_screen import LoadingScreen  # Import the loading screen

# Initialize Pygame
pygame.init()

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (32, 32, 32)
BORDER_COLOR = (89, 55, 44)

# Colors
WHITE = (255, 255, 255)
BROWN = (101, 67, 56)

# UI Element Sizes
AVATAR_SIZE = 120  # Increased from 100 to 120
PREVIEW_SIZE = 200
INPUT_BOX_WIDTH = 300
INPUT_BOX_HEIGHT = 40
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

class CharacterSelector:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Character Selection")
        
        # Load and scale character avatars
        self.character_images = {
            "boy1": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy1/boy1_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy1/boy1_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl1": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl1/girl1_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl1/girl1_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "boy2": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy2/boy2_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy2/boy2_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl2": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl2/girl2_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl2/girl2_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "boy3": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy3/boy3_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/boy3/boy3_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl3": [
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl3/girl3_closeup.png"), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load("assets/images/character-selection/girl3/girl3_portrait.png"), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            # Add more character images here
        }
        
        # Input field settings
        self.name_input = ""
        self.input_active = False
        self.font = pygame.font.Font(None, 32)
        self.selected_character = "boy1"  # Default to the first character
        self.highlight_color = (101, 67, 56)  # Brown color for highlight

        self.grid_top_margin = 50
        self.grid_bottom_margin = 50
        self.grid_height = 3 * AVATAR_SIZE + 2 * 30  # 3 rows of avatars with 30px spacing
        self.grid_y_offset = (WINDOW_HEIGHT - self.grid_height - self.grid_top_margin - self.grid_bottom_margin) // 2 + self.grid_top_margin
        self.input_box_rect = pygame.Rect(WINDOW_WIDTH - INPUT_BOX_WIDTH - 50, (WINDOW_HEIGHT - INPUT_BOX_HEIGHT) // 2 + 100, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)

    def draw_border(self):
        # Draw outer border
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        # Draw inner background
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (20, 20, WINDOW_WIDTH-40, WINDOW_HEIGHT-40))

    def draw_character_grid(self):
        # Draw 3x2 grid of character avatars
        characters = list(self.character_images.keys())
        for row in range(3):
            for col in range(2):
                index = row * 2 + col
                if index < len(characters):
                    character = characters[index]
                    x = 50 + col * (AVATAR_SIZE + 30)  # Increased spacing from 20 to 30
                    y = self.grid_y_offset + row * (AVATAR_SIZE + 30)  # Increased spacing from 20 to 30
                    if character == self.selected_character:
                        pygame.draw.rect(self.screen, self.highlight_color, (x-5, y-5, AVATAR_SIZE+10, AVATAR_SIZE+10), 3)
                    pygame.draw.rect(self.screen, WHITE, (x, y, AVATAR_SIZE, AVATAR_SIZE))
                    self.screen.blit(self.character_images[character][0], (x, y))
                    # Check for mouse click to select character
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if x < mouse_x < x + AVATAR_SIZE and y < mouse_y < y + AVATAR_SIZE:
                            self.selected_character = character

    def draw_preview(self):
        # Draw large character preview
        preview_x = WINDOW_WIDTH - PREVIEW_SIZE - 100
        preview_y = (WINDOW_HEIGHT - PREVIEW_SIZE) // 2 - 50
        pygame.draw.circle(self.screen, WHITE, 
                         (preview_x + PREVIEW_SIZE//2, preview_y + PREVIEW_SIZE//2), 
                         PREVIEW_SIZE//2)
        if self.selected_character:
            portrait = self.character_images[self.selected_character][1]
            portrait = pygame.transform.scale(portrait, (PREVIEW_SIZE, PREVIEW_SIZE))
            portrait_rect = portrait.get_rect(center=(preview_x + PREVIEW_SIZE//2, preview_y + PREVIEW_SIZE//2))
            
            # Create a mask for circular cropping
            mask = pygame.Surface((PREVIEW_SIZE, PREVIEW_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (PREVIEW_SIZE//2, PREVIEW_SIZE//2), PREVIEW_SIZE//2)
            portrait.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
            self.screen.blit(portrait, portrait_rect)

    def draw_input_field(self):
        # Draw name input field
        input_x = self.input_box_rect.x
        input_y = self.input_box_rect.y
        pygame.draw.rect(self.screen, (230, 220, 211), self.input_box_rect)
        
        # Draw "Name" label
        name_label = self.font.render("Name", True, WHITE)
        self.screen.blit(name_label, (input_x, input_y - 30))
        
        # Draw input text
        text_surface = self.font.render(self.name_input, True, (0, 0, 0))
        self.screen.blit(text_surface, (input_x + 5, input_y + 5))

    def draw_ok_button(self):
        # Draw OK button
        button_x = WINDOW_WIDTH - BUTTON_WIDTH - 50
        button_y = (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + 200
        pygame.draw.rect(self.screen, BROWN, 
                        (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Draw button text
        button_text = self.font.render("OK", True, WHITE)
        text_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH//2, 
                                               button_y + BUTTON_HEIGHT//2))
        self.screen.blit(button_text, text_rect)

        # Check for mouse click to navigate to loading screen
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x < mouse_x < button_x + BUTTON_WIDTH and button_y < mouse_y < button_y + BUTTON_HEIGHT:
                loading_screen = LoadingScreen()
                loading_screen.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    else:
                        self.name_input += event.unicode

            # Draw all elements
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_border()
            self.draw_character_grid()
            self.draw_preview()
            self.draw_input_field()
            self.draw_ok_button()
            
            pygame.display.flip()

if __name__ == "__main__":
    selector = CharacterSelector()
    selector.run()