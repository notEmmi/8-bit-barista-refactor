import pygame
import sys
import os
import json
from options import OptionsMenu
from advanced import AdvancedMenu
from keybinds import ControlsMenu

class StartMenu:
    def __init__(self, gameInstance = None):
        # Initialize Pygame
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("8-BIT BARISTA")

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)  # Background
        self.DARK_BROWN = (38, 35, 34)  # Inner background
        self.BROWN = (99, 55, 44)  # Buttons and title bar
        self.WHITE = (255, 255, 255)
        self.SHADOW_COLOR = (20, 20, 20, 180)  # Shadow opacity adjustment

        # Fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.button_font = pygame.font.Font(pygame.font.match_font('courier'), 22)

        # Check if save file exists
        self.save_file = "save_game.json"
        self.buttons = []

        # Game States
        self.MENU = "menu"
        self.GAME = "game"
        self.OPTIONS = "options"
        self.CHARACTER_SELECTION = "character_selection"
        self.CONTROLS = "controls"
        self.ADVANCED = "advanced"
        self.current_screen = self.MENU  # Start at the menu

        # Default values for user inputs (name, character, house)
        self.player_name = "Player"
        self.selected_character = "boy1"  # Default character

        self.isFromGame = False

        # Initialize the game instance only when needed
        self.currentGameInstance = None  # Initially, it's None

        # Define Buttons
        button_width, button_height = 200, 60
        button_x = (self.WIDTH - button_width) // 2
        button_spacing = 90
        button_start_y = 220

        if self.check_save_exists():
            self.buttons.append(self.Button("CONTINUE", 300, 220, 200, 60, self.load_game))
            self.buttons.append(self.Button("NEW GAME", 300, 300, 200, 60, self.start_new_game))
        else:
            self.buttons.append(self.Button("NEW GAME", 300, 250, 200, 60, self.start_new_game))

        # Add "Options" and "Exit" buttons
        self.buttons.append(self.Button("OPTIONS", button_x, button_start_y + button_spacing, button_width, button_height, self.OPTIONS))
        self.buttons.append(self.Button("EXIT", (self.WIDTH - 150) // 2, button_start_y + 2 * button_spacing, 150, 55, None))

        # Load Coffee Cup Image
        try:
            image_path = os.path.join("assets", "images", "others", "coffee.png")
            self.coffee_img = pygame.image.load(image_path)
            self.coffee_img = pygame.transform.scale(self.coffee_img, (235, 235))
        except:
            self.coffee_img = None

    def start_new_game(self):
        """Transition to character selection screen for new game."""
        print("Starting new game...")

            # Initialize the game instance
        if self.currentGameInstance is None:
            from first_page import Game
            self.currentGameInstance = Game(chosen_building=None)  # Initialize if not already

        # Initialize or reset the game state as needed
        self.currentGameInstance.player_data["name"] = self.player_name
        self.currentGameInstance.player_data["character"] = self.selected_character
        self.currentGameInstance.environment_data["day"] = 1
        self.currentGameInstance.environment_data["weather"] = "sunny"
        self.currentGameInstance.environment_data["time"] = "6:00 AM"
        
        # Transition to character selection screen
        self.current_screen = self.CHARACTER_SELECTION

    def load_game(self):
        """Load the saved game and transition to the game screen."""
        print("Loading saved game...")
        self.currentGameInstance.load_game()
        self.current_screen = self.GAME  # Transition to game screen

    def save_game(self):
        """Save the current game data to a file."""
        game_data = {
            "player": self.currentGameInstance.player_data,
            "environment": self.currentGameInstance.environment_data,
            "time": self.currentGameInstance.time_data,
        }
        with open(self.save_file, 'w') as save_file:
            json.dump(game_data, save_file)
        print("Game saved successfully!")

    def check_save_exists(self):
        """Check if a save file exists."""
        return os.path.exists(self.save_file)
    
    def draw_blurred_shadow(self, surface, rect, blur_radius=10, offset_x=8, offset_y=8, border_radius=12):
        """Draws a smooth, blurred shadow for UI elements."""
        shadow_surface = pygame.Surface((rect.width + offset_x * 2, rect.height + offset_y * 2), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 0))  # Transparent layer
        shadow_rect = pygame.Rect(offset_x, offset_y, rect.width, rect.height)
        pygame.draw.rect(shadow_surface, self.SHADOW_COLOR, shadow_rect, border_radius=border_radius)
        surface.blit(shadow_surface, (rect.x, rect.y))

    class Button:
        """UI Button with hover effects and shadows."""
        def __init__(self, text, x, y, width, height, action, border_radius=12):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = (99, 55, 44)
            self.border_radius = border_radius
            self.action = action  # Action defines which screen to switch to

        def draw(self, screen, mouse_pos, button_font, draw_blurred_shadow, DARK_BROWN, BROWN, WHITE):
            draw_blurred_shadow(screen, self.rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=self.border_radius)
            pygame.draw.rect(screen, DARK_BROWN if self.rect.collidepoint(mouse_pos) else BROWN, self.rect, border_radius=self.border_radius)
            text_surface = button_font.render(self.text, True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

        def is_clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    def show_menu(self):
        self.screen.fill(self.LIGHT_BROWN)

        # Inner Background
        center_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        self.draw_blurred_shadow(self.screen, center_rect, blur_radius=15, offset_x=4, offset_y=4, border_radius=12)
        pygame.draw.rect(self.screen, self.DARK_BROWN, center_rect, border_radius=12)

        # Title Bar
        title_rect = pygame.Rect(160, 70, 480, 85)
        self.draw_blurred_shadow(self.screen, title_rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=12)
        pygame.draw.rect(self.screen, self.BROWN, title_rect, border_radius=12)
        self.screen.blit(self.title_font.render("8-BIT BARISTA", True, self.WHITE), self.title_font.render("8-BIT BARISTA", True, self.WHITE).get_rect(center=title_rect.center))

        # Mouse Tracking
        mouse_pos = pygame.mouse.get_pos()

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen, mouse_pos, self.button_font, self.draw_blurred_shadow, self.DARK_BROWN, self.BROWN, self.WHITE)

        # Draw Coffee Cup
        if self.coffee_img:
            image_x = (self.WIDTH - self.coffee_img.get_width()) - 45
            image_y = (self.HEIGHT - self.coffee_img.get_height()) - 60
            self.screen.blit(self.coffee_img, (image_x, image_y))

    def run(self):
        running = True
        options_menu = OptionsMenu(self.currentGameInstance)  # Create an instance of OptionsMenu
        advanced_menu = AdvancedMenu()
        controls_menu = ControlsMenu()
        from character_selection import CharacterSelector  # Import CharacterSelector
        character_selector = CharacterSelector()  # Create an instance of CharacterSelector
        while running:
            events = pygame.event.get()
            self.screen.fill(self.LIGHT_BROWN)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Handle screen transitions
            if self.current_screen == self.MENU:
                self.show_menu()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in self.buttons:
                            if button.is_clicked(pygame.mouse.get_pos()):
                                if button.action:
                                    if button.text == "CONTINUE":
                                        self.load_game()
                                    if button.text == "NEW GAME":
                                        self.start_new_game()
                                    else:
                                        self.current_screen = button.action
                                if button.text == "EXIT":
                                    running = False
                                print(f"{button.text} button clicked!")
            
            elif self.current_screen == self.GAME:
                # Ensure the game instance is created if it wasn't
                if self.currentGameInstance is None:
                    from first_page import Game
                    self.currentGameInstance = Game(chosen_building=None)  # Initialize if not already
                self.currentGameInstance.run()  # Start the game loop when we enter the game screen
                running = False  # Exit the main loop to prevent further iterations if game is over

            elif self.current_screen == self.OPTIONS:
                new_screen = options_menu.show_options(events)
                if new_screen == "menu":
                    self.current_screen = self.MENU
                elif new_screen == "controls":
                    self.current_screen = self.CONTROLS
                elif new_screen == "advanced":
                    self.current_screen = self.ADVANCED

            elif self.current_screen == self.CHARACTER_SELECTION:
                character_selector.run()  # Run the character selection screen
                self.current_screen = self.GAME  # After character selection, return to menu
                print(f"Current Screen: {self.current_screen}")

            elif self.current_screen == self.ADVANCED:
                advanced_button_callback = advanced_menu.run()
                if advanced_button_callback == "options": self.current_screen = self.OPTIONS

            elif self.current_screen == self.CONTROLS:
                controls_button_callback = controls_menu.run()
                if controls_button_callback == "options": self.current_screen = self.OPTIONS

            pygame.display.flip()  # Update screen

        pygame.quit()
        sys.exit()

# Example usage
# start_menu = StartMenu()
# start_menu.run()