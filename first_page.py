import pygame
import pytmx
import os
from pygame.math import Vector2

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Screen Size
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600

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

        # Load and play background music
        self.background_music = os.path.join(self.SOUND_PATH, "1_new_life_master.mp3")
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)  # Play on repeat

    

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

    def run(self):
        # Main Game Loop
        running = True
        clock = pygame.time.Clock()
        FPS = 60

        while running:
            self.camera_surface.fill((0, 0, 0))  # Clear screen
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

            # **Camera Moves Freely Until It Hits the Map Edge**
            new_camera_x = self.player_x - self.CAMERA_WIDTH // 2
            new_camera_y = self.player_y - self.CAMERA_HEIGHT // 2

            # **Clamp Camera to Stay Within the Map Bounds**
            self.camera_x = max(0, min(new_camera_x, self.MAP_WIDTH - self.CAMERA_WIDTH))
            self.camera_y = max(0, min(new_camera_y, self.MAP_HEIGHT - self.CAMERA_HEIGHT))

            # Draw Player at Correct Position Relative to Camera
            self.camera_surface.blit(self.ANIMATION_FRAMES[self.player_direction][self.animation_index], 
                                     (self.player_x - self.camera_x, self.player_y - self.camera_y))

            # Scale up the camera surface to the main screen
            zoomed_surface = pygame.transform.scale(self.camera_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(zoomed_surface, (0, 0))

            # Handle Quit Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()  # Update display
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
