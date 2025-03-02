import pygame  # Import the pygame module
import sys  # Import the sys module
import os  # Import the os module
from Loading import LoadingScreen  # Import the LoadingScreen class
from placeholder_screen import PlaceholderScreen  # Import the PlaceholderScreen class

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
AVATAR_SIZE = 120
PREVIEW_SIZE = 200
INPUT_BOX_WIDTH = 300
INPUT_BOX_HEIGHT = 40
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# Asset directory
ASSET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/images/character-selection'))

class CharacterSelector:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Create the game window
        pygame.display.set_caption("Character Selection")  # Set the window title
        
        # Load and scale character avatars
        self.character_images = {
            "boy1": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy1/boy1_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy1/boy1_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl1": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl1/girl1_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl1/girl1_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "boy2": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy2/boy2_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy2/boy2_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl2": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl2/girl2_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl2/girl2_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "boy3": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy3/boy3_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boy3/boy3_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            "girl3": [
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl3/girl3_closeup.png")), (AVATAR_SIZE, AVATAR_SIZE)),
                pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "girl3/girl3_portrait.png")), (PREVIEW_SIZE, PREVIEW_SIZE))
            ],
            # Add more character images here
        }
        
        # Input field settings
        self.name_input = ""
        self.input_active = False
        self.font = pygame.font.Font(None, 32)
        self.selected_character = "boy1"
        self.error_message = ""

        # UI Element Positions
        self.grid_top_margin = 50
        self.grid_bottom_margin = 50
        self.grid_height = 3 * AVATAR_SIZE + 2 * 30
        self.grid_y_offset = (WINDOW_HEIGHT - self.grid_height - self.grid_top_margin - self.grid_bottom_margin) // 2 + self.grid_top_margin  # Calculate the grid y offset
        self.input_box_rect = pygame.Rect(WINDOW_WIDTH - INPUT_BOX_WIDTH - 50, (WINDOW_HEIGHT - INPUT_BOX_HEIGHT) // 2 + 100, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)  # Set the input box rectangle

        # Cursor settings
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()

        self.key_repeat_delay = 300
        self.key_repeat_interval = 50
        self.last_key_time = 0
        self.last_key = None

    def draw_border(self):
        # Draw outer border
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        # Draw inner background
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (20, 20, WINDOW_WIDTH-40, WINDOW_HEIGHT-40))

    def draw_character_grid(self):
        # Draw 3x2 grid of character avatars
        characters = list(self.character_images.keys())  # Get the list of character keys
        for row in range(3):
            for col in range(2):
                index = row * 2 + col
                if index < len(characters):
                    character = characters[index]
                    # Calculate the x and y position for the character avatar
                    x = 50 + col * (AVATAR_SIZE + 30)
                    y = self.grid_y_offset + row * (AVATAR_SIZE + 30) 

                    # Draw character avatar
                    if character == self.selected_character:
                        pygame.draw.rect(self.screen, BROWN, (x-5, y-5, AVATAR_SIZE+10, AVATAR_SIZE+10), 3)  # Draw a highlight around the selected character
                    pygame.draw.rect(self.screen, WHITE, (x, y, AVATAR_SIZE, AVATAR_SIZE))  # Draw the character avatar background
                    self.screen.blit(self.character_images[character][0], (x, y))  # Draw the character avatar
                    
                    # Check for mouse click to select character
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if x < mouse_x < x + AVATAR_SIZE and y < mouse_y < y + AVATAR_SIZE:  # Check if the mouse is over the character avatar
                            self.selected_character = character

    def draw_preview(self):
        # Draw large character preview
        preview_x = WINDOW_WIDTH - PREVIEW_SIZE - 100
        preview_y = (WINDOW_HEIGHT - PREVIEW_SIZE) // 2 - 50
        pygame.draw.circle(self.screen, WHITE, 
                         (preview_x + PREVIEW_SIZE//2, preview_y + PREVIEW_SIZE//2), 
                         PREVIEW_SIZE//2)  # Draw a white circle as the background for the preview
        if self.selected_character:
            portrait = self.character_images[self.selected_character][1]
            portrait = pygame.transform.scale(portrait, (PREVIEW_SIZE, PREVIEW_SIZE))
            portrait_rect = portrait.get_rect(center=(preview_x + PREVIEW_SIZE//2, preview_y + PREVIEW_SIZE//2))

            # Create a mask for circular cropping
            mask = pygame.Surface((PREVIEW_SIZE, PREVIEW_SIZE), pygame.SRCALPHA)  # Create a surface for the mask
            pygame.draw.circle(mask, (255, 255, 255, 255), (PREVIEW_SIZE//2, PREVIEW_SIZE//2), PREVIEW_SIZE//2)
            portrait.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)  # Apply the mask to the portrait image
            
            self.screen.blit(portrait, portrait_rect)  # Draw the portrait image on the screen

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
        
        # Draw blinking cursor
        if self.input_active and self.cursor_visible:
            cursor_x = input_x + 5 + text_surface.get_width()
            cursor_y = input_y + 5
            cursor_height = self.font.get_height()
            pygame.draw.line(self.screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
        
        # Draw error message if any
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_surface, (input_x, input_y + INPUT_BOX_HEIGHT + 10))

    def draw_ok_button(self):
        # Draw OK button
        button_x = WINDOW_WIDTH - BUTTON_WIDTH - 50
        button_y = (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + 200
        pygame.draw.rect(self.screen, BROWN, 
                (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Draw button text
        button_text = self.font.render("OK", True, WHITE)
        text_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH//2, button_y + BUTTON_HEIGHT//2))
        self.screen.blit(button_text, text_rect)

        # Check for mouse click to navigate to loading screen
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x < mouse_x < button_x + BUTTON_WIDTH and button_y < mouse_y < button_y + BUTTON_HEIGHT:
                if self.name_input.strip() == "":  # Check if the name input is empty
                    self.error_message = "Name required."
                else:
                    self.error_message = ""  # Clear the error message
                    placeholder_screen = PlaceholderScreen()
                    loading_screen = LoadingScreen(placeholder_screen.run)  # Create a loading screen instance
                    loading_screen.run()

    def handle_key_press(self, event):
        # Handle key press events
        if event.key == pygame.K_RETURN:  # If enter is pressed, submit the name
            self.input_active = False
        elif event.key == pygame.K_BACKSPACE:  # If backspace is pressed, remove the last character
            self.name_input = self.name_input[:-1]
        elif event.unicode.isalpha() and len(self.name_input) < 20:  # If the name is valid, add the character to the name input
            self.name_input += event.unicode
        else:
            if not event.unicode.isalpha() and event.key != pygame.K_LSHIFT and event.key != pygame.K_RSHIFT and event.key != pygame.K_CAPSLOCK:
                self.error_message = "Only letters."  # If the character is not a letter, show an error message
            elif len(self.name_input) >= 20:
                self.error_message = "Max 20 chars."  # If the name is too long, show an error message

    def run(self):
        # Main loop
        while True:
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()  # Get the state of all keys

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the window is closed, quit the game
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed, check for input activation
                    if self.input_box_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

                if event.type == pygame.KEYDOWN and self.input_active:  # If a key is pressed and the input is active, handle the key press
                    self.handle_key_press(event)
                    self.last_key_time = current_time
                    self.last_key = event.key

            if self.input_active and self.last_key is not None:  # Check if the input is active and a key is pressed
                if current_time - self.last_key_time > self.key_repeat_delay:  # Check if the key repeat delay has passed
                    if keys[self.last_key]:  # Check if the key is still pressed
                        if 0 <= self.last_key < 0x110000:  # Ensure the key code is within the valid range for chr()
                            self.handle_key_press(pygame.event.Event(pygame.KEYDOWN, key=self.last_key, unicode=chr(self.last_key)))  # Handle the key press
                        self.last_key_time = current_time - self.key_repeat_delay + self.key_repeat_interval  # Update the last key time

            # Toggle cursor visibility
            if current_time - self.cursor_timer > 500:  # Check if 500 milliseconds have passed
                self.cursor_visible = not self.cursor_visible  # Toggle the cursor visibility
                self.cursor_timer = current_time  # Update the cursor timer

            # Draw all elements
            self.screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color
            self.draw_border()  # Draw the border
            self.draw_character_grid()  # Draw the character grid
            self.draw_preview()  # Draw the character preview
            self.draw_input_field()  # Draw the input field
            self.draw_ok_button()  # Draw the OK button
            
            pygame.display.flip()  # Update the display


# Example usage
# selector = CharacterSelector()
# selector.run()