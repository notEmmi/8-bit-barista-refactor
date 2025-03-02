import pygame
import pytmx
import os

# Initialize Pygame
pygame.init()

# Screen Size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Camera Zoom Factor (1.5x Zoom)
ZOOM_FACTOR = 1.5

# Adjusted Screen Size for the Camera View
CAMERA_WIDTH = int(SCREEN_WIDTH / ZOOM_FACTOR)
CAMERA_HEIGHT = int(SCREEN_HEIGHT / ZOOM_FACTOR)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Game")

# File Paths
BASE_DIR = os.path.dirname(__file__)
SPRITE_PATH = os.path.join(BASE_DIR, "assets", "sprite")
MAP_PATH = os.path.join(BASE_DIR, "assets", "map")

# Load TMX Map
TMX_FILE = os.path.join(MAP_PATH, "map.tmx")
tmx_data = pytmx.load_pygame(TMX_FILE)

# Extract Tile Size
TILE_WIDTH = tmx_data.tilewidth
TILE_HEIGHT = tmx_data.tileheight
MAP_WIDTH = tmx_data.width * TILE_WIDTH
MAP_HEIGHT = tmx_data.height * TILE_HEIGHT

# Player Constants
PLAYER_SPEED = 3

# Load Individual Sprite Images
ANIMATION_FRAMES = {
    "down": [pygame.image.load(os.path.join(SPRITE_PATH, "move_down_1.png")),
             pygame.image.load(os.path.join(SPRITE_PATH, "move_down_2.png"))],
    "up": [pygame.image.load(os.path.join(SPRITE_PATH, "move_up_1.png")),
           pygame.image.load(os.path.join(SPRITE_PATH, "move_up_2.png"))],
    "left": [pygame.image.load(os.path.join(SPRITE_PATH, "move_left_1.png")),
             pygame.image.load(os.path.join(SPRITE_PATH, "move_left_2.png"))],
    "right": [pygame.image.load(os.path.join(SPRITE_PATH, "move_right_1.png")),
              pygame.image.load(os.path.join(SPRITE_PATH, "move_right_2.png"))],
    "idle_down": [pygame.image.load(os.path.join(SPRITE_PATH, "down_idle.png"))],
    "idle_up": [pygame.image.load(os.path.join(SPRITE_PATH, "up_idle.png"))],
    "idle_left": [pygame.image.load(os.path.join(SPRITE_PATH, "left_idle.png"))],
    "idle_right": [pygame.image.load(os.path.join(SPRITE_PATH, "right_idle.png"))],
}

# Get sprite size
SPRITE_WIDTH, SPRITE_HEIGHT = ANIMATION_FRAMES["down"][0].get_width(), ANIMATION_FRAMES["down"][0].get_height()

# Player Setup (Start in the middle of the map)
player_x, player_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
player_direction = "idle_down"  # Default idle position
animation_index = 0
animation_timer = 0

# Camera Position (Starts Centered)
camera_x, camera_y = player_x - CAMERA_WIDTH // 2, player_y - CAMERA_HEIGHT // 2

# Create a surface for rendering with zoom applied
camera_surface = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))

# Function to Draw Map
def draw_map(surface, cam_x, cam_y):
    """Draws the visible portion of the TMX map based on the camera position."""
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid == 0:
                    continue
                
                tile = tmx_data.get_tile_image_by_gid(gid)
                tile_x = x * TILE_WIDTH - cam_x
                tile_y = y * TILE_HEIGHT - cam_y

                # Only draw tiles that are visible within the camera view
                if -TILE_WIDTH <= tile_x < CAMERA_WIDTH and -TILE_HEIGHT <= tile_y < CAMERA_HEIGHT:
                    surface.blit(tile, (tile_x, tile_y))

# Main Game Loop
running = True
clock = pygame.time.Clock()
FPS = 60

while running:
    camera_surface.fill((0, 0, 0))  # Clear screen
    draw_map(camera_surface, camera_x, camera_y)  # Draw map to camera

    # Handle Events
    keys = pygame.key.get_pressed()
    moving = False

    # Movement Logic (Player Now Restricted to Map Bounds)
    move_x, move_y = 0, 0

    if keys[pygame.K_w]:  # Move Up
        if player_y - PLAYER_SPEED >= 0:  # Prevent going above the map
            move_y = -PLAYER_SPEED
        player_direction = "up"
        moving = True
    if keys[pygame.K_s]:  # Move Down
        if player_y + PLAYER_SPEED + SPRITE_HEIGHT <= MAP_HEIGHT:  # Prevent going below the map
            move_y = PLAYER_SPEED
        player_direction = "down"
        moving = True
    if keys[pygame.K_a]:  # Move Left
        if player_x - PLAYER_SPEED >= 0:  # Prevent going left off the map
            move_x = -PLAYER_SPEED
        player_direction = "left"
        moving = True
    if keys[pygame.K_d]:  # Move Right
        if player_x + PLAYER_SPEED + SPRITE_WIDTH <= MAP_WIDTH:  # Prevent going right off the map
            move_x = PLAYER_SPEED
        player_direction = "right"
        moving = True

    # Apply Movement (Player Now Restricted to Map Bounds)
    player_x += move_x
    player_y += move_y

    # Handle Idle Animations (When No Input is Given)
    if not moving:
        if player_direction == "up":
            player_direction = "idle_up"
        elif player_direction == "down":
            player_direction = "idle_down"
        elif player_direction == "left":
            player_direction = "idle_left"
        elif player_direction == "right":
            player_direction = "idle_right"

    # Update Animation (Only cycle between the two movement frames when moving)
    if moving:
        animation_timer += 1
        if animation_timer > 10:  # Adjust animation speed
            animation_index = (animation_index + 1) % 2  # Always alternate between 0 and 1
            animation_timer = 0
    else:
        animation_index = 0  # Reset to first frame when idle

    # **Camera Moves Freely Until It Hits the Map Edge**
    new_camera_x = player_x - CAMERA_WIDTH // 2
    new_camera_y = player_y - CAMERA_HEIGHT // 2

    # **Clamp Camera to Stay Within the Map Bounds**
    camera_x = max(0, min(new_camera_x, MAP_WIDTH - CAMERA_WIDTH))
    camera_y = max(0, min(new_camera_y, MAP_HEIGHT - CAMERA_HEIGHT))

    # Draw Player at Correct Position Relative to Camera
    camera_surface.blit(ANIMATION_FRAMES[player_direction][animation_index], 
                        (player_x - camera_x, player_y - camera_y))

    # Scale up the camera surface to the main screen
    zoomed_surface = pygame.transform.scale(camera_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(zoomed_surface, (0, 0))

    # Handle Quit Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update display
    clock.tick(FPS)

pygame.quit()
