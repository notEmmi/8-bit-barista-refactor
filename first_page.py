import pygame
import pytmx
import os
import time
from weather import Rain, Raindrop, FloorDrop, Cloudy
from toolbar import Toolbox
import interactions
import customers
import shop
import random

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        # Screen Size
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600

        # initializing rain
        self.rain = Rain()
        self.raining = False 

        # Initalize cloudy weather
        self.cloudy = Cloudy()
        self.cloudy_weather = False

        # Create Dark Rain Overlay
        self.rain_overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rain_overlay.fill((0, 0, 0, 100))  # Semi-transparent black layer (100/255 opacity)

        # Day transition
        self.current_day = 1
        self.current_weather = "sunny"
        self.last_processed_day = 0
        self.weather_icons = {
            "sunny": pygame.image.load(os.path.join("assets", "icons", "sunny.png")).convert_alpha(),
            "cloudy": pygame.image.load(os.path.join("assets", "icons", "cloudy.png")).convert_alpha(),
            "rainy": pygame.image.load(os.path.join("assets", "icons", "rainy.png")).convert_alpha()
        }
        self.is_paused = False
        self.show_new_day_prompt = False
        self.confirm_new_day = False
        self.last_game_time = time.time()

        # Camera Zoom Factor (2x Zoom)
        self.ZOOM_FACTOR = 2.0
        ## rectangles for click detection
        self.cafe_rect = pygame.Rect(377, 309, 77, 84)

        # Adjusted Screen Size for the Camera View
        self.CAMERA_WIDTH = int(self.SCREEN_WIDTH / self.ZOOM_FACTOR)
        self.CAMERA_HEIGHT = int(self.SCREEN_HEIGHT / self.ZOOM_FACTOR)

        # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("My Pygame Game")

        # File Paths
        self.BASE_DIR = os.path.dirname(__file__)
        self.SPRITE_PATH = os.path.join(self.BASE_DIR, "assets", "sprite")
        self.MAP_PATH = os.path.join(self.BASE_DIR, "assets", "map")
        self.SOUND_PATH = os.path.join(self.BASE_DIR, "assets", "sounds")

        # Load TMX Map
        self.load_map(os.path.join(self.MAP_PATH, "map.tmx"))

        # Extract Tile Size
        self.TILE_WIDTH = self.tmx_data.tilewidth
        self.TILE_HEIGHT = self.tmx_data.tileheight
        self.MAP_WIDTH = self.tmx_data.width * self.TILE_WIDTH
        self.MAP_HEIGHT = self.tmx_data.height * self.TILE_HEIGHT

        # Player Constants
        self.PLAYER_SPEED = 2

        # Load Rain Drop Sprites
        self.RAIN_SPRITES = [
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_3.png")).convert_alpha(),
        ]

        # Load Floor Drop Sprites
        self.FLOOR_SPRITES = [
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_3.png")).convert_alpha(),
        ]

        for sprite in self.FLOOR_SPRITES:
            sprite.set_colorkey((0, 0, 0))  # Remove black background for transparency

        # Initialize Rain system with loaded textures
        self.rain = Rain(rain_sprites=self.RAIN_SPRITES, floor_sprites=self.FLOOR_SPRITES)

        # Load Individual Sprite Images
        self.ANIMATION_FRAMES = {
            "down": [pygame.image.load(os.path.join(self.SPRITE_PATH, "down_1.png")),
                 pygame.image.load(os.path.join(self.SPRITE_PATH, "down_2.png"))],
            "up": [pygame.image.load(os.path.join(self.SPRITE_PATH, "up_1.png")),
               pygame.image.load(os.path.join(self.SPRITE_PATH, "up_2.png"))],
            "left": [pygame.image.load(os.path.join(self.SPRITE_PATH, "left_1.png")),
                 pygame.image.load(os.path.join(self.SPRITE_PATH, "left_2.png"))],
            "right": [pygame.image.load(os.path.join(self.SPRITE_PATH, "right_1.png")),
                  pygame.image.load(os.path.join(self.SPRITE_PATH, "right_2.png"))],
            "idle_down": [pygame.image.load(os.path.join(self.SPRITE_PATH, "down_idle.png"))],
            "idle_up": [pygame.image.load(os.path.join(self.SPRITE_PATH, "up_idle.png"))],
            "idle_left": [pygame.image.load(os.path.join(self.SPRITE_PATH, "left_idle.png"))],
            "idle_right": [pygame.image.load(os.path.join(self.SPRITE_PATH, "right_idle.png"))],
        }

        # Apply transparency fix by setting colorkey for character sprites
        for direction, frames in self.ANIMATION_FRAMES.items():
            for i in range(len(frames)):
                frames[i] = frames[i].convert_alpha()  # Ensure transparency is preserved
                frames[i].set_colorkey((0, 0, 0))  # Remove black background (if transparency is lost)

        # Get sprite size
        self.SPRITE_WIDTH, self.SPRITE_HEIGHT = self.ANIMATION_FRAMES["down"][0].get_width(), self.ANIMATION_FRAMES["down"][0].get_height()

        # Player Setup (Start in the middle of the map)
        self.player_x, self.player_y = self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2
        self.player_direction = "idle_down"  # Default idle position
        self.animation_index = 0
        self.animation_timer = 0

        # Camera Position (Starts Centered)
        self.camera_x, self.camera_y = self.player_x - self.CAMERA_WIDTH // 2, self.player_y - self.CAMERA_HEIGHT // 2

        # Create a surface for rendering with zoom applied
        self.camera_surface = pygame.Surface((self.CAMERA_WIDTH, self.CAMERA_HEIGHT))

        # Game Time System (Stardew Valley Timing)
        self.SECONDS_PER_GAME_MINUTE = 0.7  # 10 minutes = 7 seconds in real life
        self.GAME_START_HOUR = 6  # 6:00 AM
        self.game_start_time = time.time()  # Real-world start time
        self.time_multiplier = 1  # Normal speed, increased when pressing ''
      

        # Load and play background music
        self.background_music = os.path.join(self.SOUND_PATH, "1_new_life_master.mp3")
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)  # Play on repeat

        self.toolbox = Toolbox()

    def load_map(self, map_file):
        self.tmx_data = pytmx.load_pygame(map_file)
        self.collidable_objects = []  # Reset collision list

        # Look for a dedicated collision layer
        for obj in self.tmx_data.objects:
            if obj.name == "Collisions" or obj.properties.get("collidable", False):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.collidable_objects.append(rect)

    def move_player(self, move_x, move_y):
        new_x = self.player_x + move_x
        new_y = self.player_y + move_y

        # Define the player's hitbox (adjust padding if necessary)
        hitbox_padding_x = 0
        hitbox_padding_y = 5
        player_hitbox = pygame.Rect(
            new_x + hitbox_padding_x, 
            new_y + hitbox_padding_y, 
            self.SPRITE_WIDTH - 2 * hitbox_padding_x, 
            self.SPRITE_HEIGHT - 2 * hitbox_padding_y
        )

        # Check if the new position collides with any object
        for obj in self.collidable_objects:
            if player_hitbox.colliderect(obj):
                return  # Collision detected, don't move

        # No collision, update player position
        self.player_x = new_x
        self.player_y = new_y

    def draw_map(self, surface, cam_x, cam_y):
        # Draw the tile layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid == 0:
                        continue  # Skip empty tiles
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    tile_x = x * self.TILE_WIDTH - cam_x
                    tile_y = y * self.TILE_HEIGHT - cam_y

                    # Only draw tiles visible within the camera view
                    if -self.TILE_WIDTH <= tile_x < self.CAMERA_WIDTH and -self.TILE_HEIGHT <= tile_y < self.CAMERA_HEIGHT:
                        surface.blit(tile, (tile_x, tile_y))
        
        # Draw objects (Trees, buildings, etc.)
        for obj in self.tmx_data.objects:
            obj_x = obj.x - cam_x
            obj_y = obj.y - cam_y

            if obj.gid:  # If object has an image
                image = self.tmx_data.get_tile_image_by_gid(obj.gid)
                if image:
                    surface.blit(image, (obj_x, obj_y))
        
        # Debug: Draw red collision boxes
        # for rect in self.collidable_objects:
        #     pygame.draw.rect(surface, (255, 0, 0), 
        #                     (rect.x - cam_x, rect.y - cam_y, rect.width, rect.height), 2)

    def get_game_time(self):
        """Converts real-time seconds to in-game hours and minutes."""
        if self.is_paused:
            # Return the last calculated time (freeze the clock)
            elapsed_time = (self.last_game_time - self.game_start_time) * self.time_multiplier
        else:
            # Calculate elapsed time normally
            elapsed_time = (time.time() - self.game_start_time) * self.time_multiplier
            self.last_game_time = time.time()  # Store the last calculated time

        game_minutes = int(elapsed_time / self.SECONDS_PER_GAME_MINUTE)
        game_hour = (self.GAME_START_HOUR + game_minutes // 60) % 24
        game_minute = game_minutes % 60

        return game_hour, game_minute
    
    def set_game_time(self, hour, minute):
        """
        Set the game time to a specific hour and minute.
        """
        # Calculate the total minutes since midnight
        total_minutes_since_midnight = hour * 60 + minute

        # Calculate the total minutes since GAME_START_HOUR (6:00 AM)
        # GAME_START_HOUR is 6, so 6 * 60 = 360 minutes
        total_minutes_since_game_start = total_minutes_since_midnight - (self.GAME_START_HOUR * 60)

        # If the result is negative, it means the time is before 6:00 AM
        # Add 24 hours (1440 minutes) to handle the wrap-around
        if total_minutes_since_game_start < 0:
            total_minutes_since_game_start += 24 * 60

        # Update game_start_time to reflect the new time
        self.game_start_time = time.time() - (total_minutes_since_game_start * self.SECONDS_PER_GAME_MINUTE)

    def is_night_time(self):
        """Returns True if the current game time is night (after 5:30 PM or before 6 AM)."""
        game_hour, game_minute = self.get_game_time()
        total_minutes = game_hour * 60 + game_minute  # Convert to total minutes since midnight

        return total_minutes >= 1050 or total_minutes < 360  # 1050 = 5:30 PM, 360 = 6:00 AM
   
    def draw_night_filter(self):
        """Applies a transparent gradient for nighttime effect without duplicating overlays."""
        game_hour, game_minute = self.get_game_time()
        total_minutes = game_hour * 60 + game_minute

        start_night_transition = 17 * 60 + 30  # 5:30 PM
        end_night_transition = 18 * 60  # 6:00 PM

        start_morning_transition = 5 * 60 + 30  # 5:30 AM
        end_morning_transition = 6 * 60  # 6:00 AM

        transition_progress = 0  # Default to no overlay

        # Determine transition progress
        if start_night_transition <= total_minutes <= end_night_transition:  
            # Nighttime transition (5:30 PM - 5:40 PM)
            transition_progress = (total_minutes - start_night_transition) / (end_night_transition - start_night_transition)
        elif start_morning_transition <= total_minutes <= end_morning_transition:  
            # Morning transition (5:50 AM - 6:00 AM) → Fade out night filter
            transition_progress = 1 - ((total_minutes - start_morning_transition) / (end_morning_transition - start_morning_transition))
        elif total_minutes > end_night_transition or total_minutes < start_morning_transition:
            # Fully dark at night
            transition_progress = 1

        # If fully daylight, return 0 alpha (no effect)
        if transition_progress == 0:
            return 0  

        # Calculate alpha value for overlay
        alpha_value = int(transition_progress * 180)  # Max opacity at night

        return alpha_value

    def check_new_day(self):
        game_hour, game_minute = self.get_game_time()
        total_game_minutes = game_hour * 60 + game_minute
        
        # Calculate current day based on time passed
        days_passed = (total_game_minutes - 330) // (24 * 60) + 1  # 330 = 5:30 AM
        
        if days_passed > self.current_day:
            self.current_day = days_passed
            # First day is always sunny, others random
            if self.current_day == 1:
                self.current_weather = "sunny"
            else:
                self.current_weather = random.choice(["sunny", "cloudy", "rainy"])
            
            # Set weather states based on new weather
            self.raining = self.current_weather == "rainy"
            self.cloudy_weather = self.current_weather == "cloudy"
            print(f"Day {self.current_day} - Weather: {self.current_weather}")
    
    def check_for_new_day_prompt(self):
        game_hour, game_minute = self.get_game_time()
        
        # Check if it's 2:00 AM and the prompt hasn't been shown yet
        if game_hour == 2 and game_minute == 0 and not self.show_new_day_prompt:
            self.is_paused = True  # Pause the game
            self.show_new_day_prompt = True  # Show the prompt
    
    def draw_new_day_prompt(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Dark semi-transparent overlay
        self.screen.blit(overlay, (0, 0))

        # Create a dialog box
        dialog_width = 500
        dialog_height = 150
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2

        pygame.draw.rect(self.screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # Draw the prompt text
        prompt_text = self.font.render("Your character is exhausted.", True, (255, 255, 255))
        prompt_text2 = self.font.render("Press [Enter] to start a new day.", True, (255, 255, 255))

        text_rect = prompt_text.get_rect(center=(self.SCREEN_WIDTH // 2, dialog_y + 50))
        text_rect2 = prompt_text2.get_rect(center=(self.SCREEN_WIDTH // 2, dialog_y + 90))

        self.screen.blit(prompt_text, text_rect)
        self.screen.blit(prompt_text2, text_rect2)
        
    def draw_hud(self):
        """Displays 'Day X' on top, with the Weather Icon and Clock properly aligned at the top-right."""

        # Define Panel Dimensions & Styling
        panel_x_margin = 12  # Space between panel and screen edges
        panel_y_margin = 8
        panel_width = 115  # Unified width
        panel_height = 65  # Height to fit stacked elements
        border_radius = 8  # Rounded corners

        # Load a Smaller & Thinner Font
        clock_font = pygame.font.Font(None, 30)  # Smaller size & thinner weight
        day_font = pygame.font.Font(None, 25)  # Smaller size & thinner weight

        # Create HUD Panel Background
        hud_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(
            hud_surface, (99, 55, 44, 240), (0, 0, panel_width, panel_height), border_radius=border_radius
        )

        # "Day X" - Positioned at the top with internal padding
        day_text = day_font.render(f"Day {self.current_day}", True, (255, 255, 255))
        day_rect = day_text.get_rect(midtop=(panel_width // 2, panel_y_margin))  # Centered horizontally
        hud_surface.blit(day_text, day_rect.topleft)

        # Weather Icon - Adjust Position Based on Type
        if self.current_weather in self.weather_icons:
            weather_icon = pygame.transform.scale(self.weather_icons[self.current_weather], (28, 28))
            icon_x = 8  # Fixed left alignment

            # Adjust icon height based on weather type
            if self.current_weather == "sunny":
                icon_y = day_rect.bottom + 5  # Default position
            elif self.current_weather in ["cloudy", "rainy"]:
                icon_y = day_rect.bottom + 2  # Move up slightly for balance
            else:
                icon_y = day_rect.bottom + 5  # Default fallback

            hud_surface.blit(weather_icon, (icon_x, icon_y))
        else:
            print(f"WARNING: Missing weather icon for {self.current_weather}")

        # Clock - Fixed Position (Independent)
        clock_text = f"{self.get_game_time()[0]:02}:{self.get_game_time()[1]:02}"
        time_surface = clock_font.render(clock_text, True, (255, 255, 255))
        
        clock_x = panel_width - 70  # Shift clock right, away from the icon
        clock_y = day_rect.bottom + 8  # Position slightly lower for visual balance

        hud_surface.blit(time_surface, (clock_x, clock_y))  # Now truly independent

        # Move Panel to the Top-Right of the Screen with Proper Margins
        screen_x = self.SCREEN_WIDTH - panel_width - panel_x_margin  # Fixed position
        screen_y = panel_y_margin  # Fixed vertical margin
        self.screen.blit(hud_surface, (screen_x, screen_y))

    def is_night_time(self):
        """Returns True if the current game time is night (after 5:30 PM or before 6 AM)."""
        game_hour, game_minute = self.get_game_time()
        total_minutes = game_hour * 60 + game_minute  # Convert to total minutes since midnight

        return total_minutes >= 1050 or total_minutes < 360  # 1050 = 5:30 PM, 360 = 6:00 AM

    def handle_input(self):
        """Handles keyboard input, including time acceleration."""
        keys = pygame.key.get_pressed()

        # Keybind 'b' accelerates the time
        if not self.is_paused:
            new_multiplier = 10 if keys[pygame.K_b] else 1
            if new_multiplier != self.time_multiplier:
                elapsed_time = time.time() - self.game_start_time
                self.game_start_time = time.time() - (elapsed_time * self.time_multiplier / new_multiplier)
                self.time_multiplier = new_multiplier

        if keys[pygame.K_TAB]:
            interactions.runInteractions()
        if keys[pygame.K_CAPSLOCK]:
            customers.runCustomers()
        if keys[pygame.K_LSHIFT]:
            shop.runShop()

        # Set time to 5pm by pressing 'n'
        if keys[pygame.K_n] and not self.is_paused: 
            self.set_game_time(17, 0)

        # Set time to 1 am by pressing 'm'
        if keys[pygame.K_m] and not self.is_paused:
            self.set_game_time(1,30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Toggle rain when 'R' is pressed
                    self.raining = not self.raining
                    print(f"Rain Enabled: {self.raining}")  # Debug message
                if event.key == pygame.K_c:  # Toggle cloudy weather when 'C' is pressed
                    self.cloudy_weather = not self.cloudy_weather
                    print(f"Cloudy Weather Enabled: {self.cloudy_weather}")  # Debug message 
                if self.show_new_day_prompt:  # Handle new day prompt input
                    if event.key == pygame.K_RETURN:  # Enter key
                        self.time_multiplier = 1
                        self.confirm_new_day = True
                        self.show_new_day_prompt = False
                        self.is_paused = False  # Unpause the game

            ##### handle click on rectange event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = event.pos
                        print(mouse_x, mouse_y)
                        adjusted_mouse_x = (mouse_x // self.ZOOM_FACTOR) + self.camera_x
                        adjusted_mouse_y = (mouse_y // self.ZOOM_FACTOR) + self.camera_y
                        if self.cafe_rect.collidepoint(adjusted_mouse_x, adjusted_mouse_y):
                         print("Cafe Clicked!")        

    def use_tool(self, tile_x, tile_y):
        print(f"Using tool at tile ({tile_x}, {tile_y}) with selected tool {self.toolbox.selected_tool}")
        
        if self.toolbox.selected_tool == -1:
            print("No tool selected")
            return
        
        if self.toolbox.selected_tool == 0:
            print("Using hoe")
            
            # Check if tile is tilled (id 12 on layer "Dirt")
            dirt_layer = self.tmx_data.get_layer_by_name("Dirt")
            
           
            # Check specific tile value:
            print(f"Tile at ({tile_x}, {tile_y}): {dirt_layer.data[tile_y][tile_x]}")

            if dirt_layer:
                dirt_id = 21  # Replace with the correct GID for tilled soil

                tile_gid = dirt_layer.data[tile_y][tile_x]


                if tile_gid != dirt_id:
                    # Check if the tile is not collidable
                    dirt_layer.data[tile_y][tile_x] = dirt_id
                    self.update_map("Dirt", dirt_layer.data)
                
        elif self.toolbox.selected_tool == 1:
            print("Using another tool")
   
    def update_map(self, layer_name, new_data):
        for layer in self.tmx_data.visible_layers:
            if layer.name == layer_name:
                layer.data = new_data
                break
        
    def run(self):
        # Main Game Loop
        running = True
        clock = pygame.time.Clock()
        FPS = 60

        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            self.handle_input() # Handle key inputs

            # Check for new day prompt at 2:00 AM
            self.check_for_new_day_prompt()

            self.pause_game_time = False

            # If the user confirmed a new day, reset time and advance day
            if self.confirm_new_day:
                self.set_game_time(5, 30)  # Move time reset here
                self.current_day += 1
                self.current_weather = random.choice(["sunny", "cloudy", "rainy"])
                self.raining = self.current_weather == "rainy"
                self.cloudy_weather = self.current_weather == "cloudy"
                self.confirm_new_day = False  # Reset confirmation flag
                print(f"New day started at 5:30 AM. Day {self.current_day} - Weather: {self.current_weather}")

            # Only update game logic if not paused
            if not self.is_paused:
                self.draw_map(self.camera_surface, self.camera_x, self.camera_y)

                # Handle Events
                keys = pygame.key.get_pressed()
                moving = False

                # Movement Logic (Player Now Restricted to Map Bounds)
                move_x, move_y = 0, 0

                if keys[pygame.K_w]:  # Move Up
                    if self.player_y - self.PLAYER_SPEED >= 0:  # Prevent going above the map
                        move_y = -self.PLAYER_SPEED
                    self.player_direction = "up"
                    moving = True
                if keys[pygame.K_s]:  # Move Down
                    if self.player_y + self.PLAYER_SPEED + self.SPRITE_HEIGHT <= self.MAP_HEIGHT:  # Prevent going below the map
                        move_y = self.PLAYER_SPEED
                    self.player_direction = "down"
                    moving = True
                if keys[pygame.K_a]:  # Move Left
                    if self.player_x - self.PLAYER_SPEED >= 0:  # Prevent going left off the map
                        move_x = -self.PLAYER_SPEED
                    self.player_direction = "left"
                    moving = True
                if keys[pygame.K_d]:  # Move Right
                    if self.player_x + self.PLAYER_SPEED + self.SPRITE_WIDTH <= self.MAP_WIDTH:  # Prevent going right off the map
                        move_x = self.PLAYER_SPEED
                    self.player_direction = "right"
                    moving = True


                # Apply Movement (Player Now Restricted to Map Bounds)
                self.move_player(move_x, move_y)

                # Handle Idle Animations (When No Input is Given)
                if not moving:
                    if self.player_direction == "up":
                        self.player_direction = "idle_up"
                    elif self.player_direction == "down":
                        self.player_direction = "idle_down"
                    elif self.player_direction == "left":
                        self.player_direction = "idle_left"
                    elif self.player_direction == "right":
                        self.player_direction = "idle_right"

                # Update Animation (Only cycle between the two movement frames when moving)
                if moving:
                    self.animation_timer += 1
                    if self.animation_timer > 10:  # Adjust animation speed
                        self.animation_index = (self.animation_index + 1) % 2  # Always alternate between 0 and 1
                        self.animation_timer = 0
                else:
                    self.animation_index = 0  # Reset to first frame when idle

                # Camera Moves Freely Until It Hits the Map Edge
                new_camera_x = self.player_x - self.CAMERA_WIDTH // 2
                new_camera_y = self.player_y - self.CAMERA_HEIGHT // 2

                # Clamp Camera to Stay Within the Map Bounds
                self.camera_x = max(0, min(new_camera_x, self.MAP_WIDTH - self.CAMERA_WIDTH))
                self.camera_y = max(0, min(new_camera_y, self.MAP_HEIGHT - self.CAMERA_HEIGHT))

                # Draw Player at Correct Position Relative to Camera
                self.camera_surface.blit(self.ANIMATION_FRAMES[self.player_direction][self.animation_index], 
                                        (self.player_x - self.camera_x, self.player_y - self.camera_y))

                # Scale up the camera surface to the main screen
                zoomed_surface = pygame.transform.scale(self.camera_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                # Get nighttime alpha level
                night_alpha = self.draw_night_filter()  
                rain_alpha = 80 if self.raining else 0

                # Initialize overlay with full transparency by default
                overlay = pygame.Surface((zoomed_surface.get_size()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 0))  # Fully transparent by default

                # Apply overlay only when it's night or raining
                if self.is_night_time():
                    overlay.fill((0, 0, 0, night_alpha))  # Adjust opacity

                if self.raining:
                    rain_overlay = pygame.Surface((zoomed_surface.get_size()), pygame.SRCALPHA)
                    rain_overlay.fill((0,0,0, rain_alpha))
                    overlay.blit(rain_overlay, (0,0))
                
                if self.cloudy_weather:  # Draw the cloudy overlay if enabled
                    self.cloudy.draw(overlay)  # Draw the cloudy effect on the overlay

                # Now, overlay is always defined before blitting
                zoomed_surface.blit(overlay, (0, 0))  
                
                # Draw the toolbox
                #self.toolbox.draw(self.screen)

                # Handle tool selection with number keys
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_5:
                            self.toolbox.select_tool(event.key - pygame.K_1)
                        if pygame.K_0 == event.key or pygame.K_6 <= event.key <= pygame.K_9:
                            self.toolbox.select_tool(-1)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            mouse_x, mouse_y = event.pos

                            # Adjust mouse position to account for camera and zoom factor
                            adjusted_mouse_x = (mouse_x // self.ZOOM_FACTOR) + self.camera_x
                            adjusted_mouse_y = (mouse_y // self.ZOOM_FACTOR) + self.camera_y

                            # Calculate the tile position based on the adjusted mouse position
                            tile_x = adjusted_mouse_x // self.TILE_WIDTH
                            tile_y = adjusted_mouse_y // self.TILE_HEIGHT
                            print(f"Mouse Position: ({mouse_x}, {mouse_y})")
                            print(f"Adjusted Mouse Position: ({adjusted_mouse_x}, {adjusted_mouse_y})")
                            print(f"Tile Coordinates: ({tile_x}, {tile_y})")


                            # Use the tool on the clicked tile
                            self.use_tool(int(tile_x), int(tile_y))

                # Update & Draw Rain (Only if raining)
                if self.raining:
                    self.rain.update(self.camera_x, self.camera_y)
                    self.rain.draw(zoomed_surface)  # Draw all rain elements (drops + floor splashes)

            # Blit the final zoomed surface to the screen
            self.screen.blit(zoomed_surface, (0, 0))
            
            self.toolbox.draw(self.screen)

            # Draw the new day prompt if active
            if self.show_new_day_prompt:
                self.draw_new_day_prompt()

            # Ensure weather icon is updated dynamically
            if self.current_weather in self.weather_icons:
                self.current_weather_icon = self.weather_icons[self.current_weather]
            else:
                self.current_weather_icon = None  # Fallback if missing
            
            # Draw HUD
            self.draw_hud()

            pygame.display.flip()  # Update display
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()