import pygame
import pytmx
import os
import time
from weather import Rain, Raindrop, FloorDrop
from toolbar import Toolbox

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

        # Create Dark Rain Overlay
        self.rain_overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rain_overlay.fill((0, 0, 0, 100))  # Semi-transparent black layer (100/255 opacity)

        # Camera Zoom Factor (2x Zoom)
        self.ZOOM_FACTOR = 2.0

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
        self.time_multiplier = 1  # Normal speed, increased when pressing '1'
      

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
        elapsed_time = (time.time() - self.game_start_time) * self.time_multiplier
        game_minutes = int(elapsed_time / self.SECONDS_PER_GAME_MINUTE)
        game_hour = (self.GAME_START_HOUR + game_minutes // 60) % 24
        game_minute = game_minutes % 60
        return game_hour, game_minute

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
        alpha_value = int(transition_progress * 225)  # Max opacity at night

        return alpha_value

    def draw_time_display(self):
        """Displays the current in-game time on the top right of the screen."""
        game_hour, game_minute = self.get_game_time()
        time_text = f"{game_hour:02}:{game_minute:02}"
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.SCREEN_WIDTH-10, 10))
        pygame.draw.rect(self.screen,(0,0,0,150), text_rect)

        self.screen.blit(text_surface, text_rect.topleft)

    def handle_input(self):
        """Handles keyboard input, including time acceleration."""
        keys = pygame.key.get_pressed()

        new_multiplier = 10 if keys[pygame.K_1] else 1  # Determine new multiplier
        
        if new_multiplier != self.time_multiplier:  # Only update if multiplier changed
            elapsed_time = time.time() - self.game_start_time  # Get current elapsed time
            self.game_start_time = time.time() - (elapsed_time * self.time_multiplier / new_multiplier)  
            self.time_multiplier = new_multiplier  # Update the multiplier

        # Set time to 5pm
        if keys[pygame.K_5]: 
            self.game_start_time = time.time() - ((17 - self.GAME_START_HOUR) * 60 * self.SECONDS_PER_GAME_MINUTE)

        # Set time to 5am
        if keys[pygame.K_6]:
            self.game_start_time = time.time() - ((5 * 60 - self.GAME_START_HOUR * 60) * self.SECONDS_PER_GAME_MINUTE)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Toggle rain when 'R' is pressed
                    self.raining = not self.raining
                    print(f"Rain Enabled: {self.raining}")  # Debug message

    def get_game_time(self):
        """Converts real-time seconds to in-game hours and minutes."""
        elapsed_time = (time.time() - self.game_start_time) * self.time_multiplier
        game_minutes = int(elapsed_time / self.SECONDS_PER_GAME_MINUTE)
        game_hour = (self.GAME_START_HOUR + game_minutes // 60) % 24
        game_minute = game_minutes % 60
        return game_hour, game_minute

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
        alpha_value = int(transition_progress * 225)  # Max opacity at night

        return alpha_value

    def draw_time_display(self):
        """Displays the current in-game time on the top right of the screen."""
        game_hour, game_minute = self.get_game_time()
        time_text = f"{game_hour:02}:{game_minute:02}"
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(self.SCREEN_WIDTH-10, 10))
        pygame.draw.rect(self.screen,(0,0,0,150), text_rect)

        self.screen.blit(text_surface, text_rect.topleft)

    def handle_input(self):
        """Handles keyboard input, including time acceleration."""
        keys = pygame.key.get_pressed()

        new_multiplier = 10 if keys[pygame.K_1] else 1  # Determine new multiplier
        
        if new_multiplier != self.time_multiplier:  # Only update if multiplier changed
            elapsed_time = time.time() - self.game_start_time  # Get current elapsed time
            self.game_start_time = time.time() - (elapsed_time * self.time_multiplier / new_multiplier)  
            self.time_multiplier = new_multiplier  # Update the multiplier

        # Set time to 5pm
        if keys[pygame.K_5]: 
            self.game_start_time = time.time() - ((17 - self.GAME_START_HOUR) * 60 * self.SECONDS_PER_GAME_MINUTE)

        # Set time to 5am
        if keys[pygame.K_6]:
            self.game_start_time = time.time() - ((5 * 60 - self.GAME_START_HOUR * 60) * self.SECONDS_PER_GAME_MINUTE)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Toggle rain when 'R' is pressed
                    self.raining = not self.raining
                    print(f"Rain Enabled: {self.raining}")  # Debug message

    def run(self):
        # Main Game Loop
        running = True
        clock = pygame.time.Clock()
        FPS = 60

        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            self.handle_input() # Handle key inputs
            self.draw_map(self.camera_surface, self.camera_x, self.camera_y)  # Draw map to camera

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

            # Now, overlay is always defined before blitting
            zoomed_surface.blit(overlay, (0, 0))  

            # Blit the final zoomed surface to the screen
            self.screen.blit(zoomed_surface, (0, 0))
            
            # Draw the toolbox
            self.toolbox.draw(self.screen)

            # Handle tool selection with number keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_5:
                        self.toolbox.select_tool(event.key - pygame.K_1)

            # Update & Draw Rain (Only if raining)
            if self.raining:
                self.rain.update(self.camera_x, self.camera_y)
                self.rain.draw(self.screen)
                
            # Draw Clock
            self.draw_time_display()

            # Update & Draw Rain (Only if raining)
            if self.raining:
                self.rain.update(self.camera_x, self.camera_y)
                self.rain.draw(self.screen)
                
            # Draw Clock
            self.draw_time_display()

            pygame.display.flip()  # Update display
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()