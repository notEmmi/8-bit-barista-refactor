import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set a display mode (Fixes "No video mode has been set" error)
screen = pygame.display.set_mode((800, 600))

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RAIN_COUNT = 50
FLOOR_DROP_COUNT = 10  
RAIN_SPEED_X = -16  
RAIN_SPEED_Y = 26  
RAIN_COLOR = (80, 150, 255, 150)  # Blueish with transparency (RGBA)
RAIN_OPACITY = 150  # 150 out of 255 (semi-transparent)
DROP_SIZE = (8, 16)  # Raindrop size

# Asset Directory
BASE_DIR = os.path.dirname(__file__)
RAIN_ASSET_DIR = os.path.join(BASE_DIR, "assets", "rain")

# Function to load, resize, and apply color & opacity to raindrop images
def load_and_modify_raindrop(image_path):
    """Loads, resizes, and applies color & opacity to a raindrop"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Raindrop image not found: {image_path}")

    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, DROP_SIZE)  # Resize

    # Create a new transparent surface
    colored_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    colored_image.fill(RAIN_COLOR)  # Apply color with transparency
    image.blit(colored_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Blend color
    return image

# Function to load, proportionally scale, and apply opacity to floor splashes
def load_and_modify_floor(image_path):
    """Loads floor splash image, scales it, and applies opacity"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Floor splash image not found: {image_path}")

    image = pygame.image.load(image_path).convert_alpha()
    print(f"Loaded floor sprite: {image_path}")  # Confirm it loads correctly
    
    # Maintain aspect ratio while making it fit within the raindrop's height
    original_width, original_height = image.get_size()
    scale_factor = DROP_SIZE[1] / original_height  # Scale based on height (10px)
    
    new_width = int(original_width * scale_factor)  # Maintain width proportion
    new_height = int(original_height * scale_factor)  # Should match raindrop height
    image = pygame.transform.scale(image, (new_width, new_height))

    # Create a semi-transparent surface
    transparent_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    transparent_surface.fill((255, 255, 255, RAIN_OPACITY))  # Apply opacity
    image.blit(transparent_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Blend transparency
    return image

# Load and modify raindrop images
RAIN_SPRITES = [
    load_and_modify_raindrop(os.path.join(RAIN_ASSET_DIR, "drop_1.png")),
    load_and_modify_raindrop(os.path.join(RAIN_ASSET_DIR, "drop_2.png")),
    load_and_modify_raindrop(os.path.join(RAIN_ASSET_DIR, "drop_3.png"))
]

# Load and proportionally resize floor splash images with opacity
FLOOR_SPRITES = [
    load_and_modify_floor(os.path.join(RAIN_ASSET_DIR, "floor_1.png")),
    load_and_modify_floor(os.path.join(RAIN_ASSET_DIR, "floor_2.png")),
    load_and_modify_floor(os.path.join(RAIN_ASSET_DIR, "floor_3.png"))
]

class Raindrop(pygame.sprite.Sprite):
    """Falling raindrop class, moves diagonally from top-right to bottom-left"""
    def __init__(self):
        super().__init__()
        self.image = random.choice(RAIN_SPRITES).copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH * 2)  
        self.rect.y = random.randint(-SCREEN_HEIGHT * 2, 0)  
        self.speed_x = RAIN_SPEED_X + random.randint(-2, 2)  
        self.speed_y = RAIN_SPEED_Y + random.randint(-3, 3)  

    def update(self, cam_x, cam_y, floor_group):
        """Move raindrop diagonally and check for ground collision relative to camera"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # If the raindrop reaches the ground, create a splash at its final X position
        if self.rect.y > SCREEN_HEIGHT:
            if random.random() < 0.4:  # 40% chance to create a floor splash
                # Convert to STATIC screen coordinates when raindrop lands
                screen_x = self.rect.x - cam_x  # Convert world to screen position
                screen_y = random.randint(0, SCREEN_HEIGHT)  # Fully random Y position

                # Ensure floor splashes appear in correct screen locations and NEVER move
                floor_group.add(FloorDrop(screen_x, screen_y))

            # Reset raindrop position after it falls
            self.rect.y = random.randint(-SCREEN_HEIGHT * 2, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH * 2)

class FloorDrop(pygame.sprite.Sprite):
    """Raindrop splash effect that stays FIXED in place (NOT moving with the camera)."""
    def __init__(self, screen_x, screen_y):
        super().__init__()
        self.original_image = random.choice(FLOOR_SPRITES).convert_alpha()  # Ensure transparency
        self.image = self.original_image.copy()  # Preserve original
        self.rect = self.image.get_rect()

        # Store screen position at the moment of creation
        self.rect.x = max(0, min(screen_x, SCREEN_WIDTH - self.rect.width))  
        self.rect.y = max(0, min(screen_y, SCREEN_HEIGHT - self.rect.height))

        self.lifetime = 30  # Frames before disappearing
        self.alpha = 200  # Initial opacity (out of 255)

    def update(self):
        """Reduce lifetime of splash and gradually fade out."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Remove when expired

        # Gradually fade out
        self.alpha -= 8  
        if self.alpha < 0:
            self.alpha = 0

        # Apply correct transparency using set_alpha()
        self.image = self.original_image.copy().convert_alpha()
        self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)

class Rain:
    """Manages raindrops and floor splashes"""
    def __init__(self):
        self.raindrops = pygame.sprite.Group()
        self.floor_splashes = pygame.sprite.Group()
        for _ in range(RAIN_COUNT):
            self.raindrops.add(Raindrop())

    def update(self, cam_x, cam_y):
        """Update rain movement relative to camera"""
        self.raindrops.update(cam_x, cam_y, self.floor_splashes)
        self.floor_splashes.update()

    def draw(self, screen):
        """Draw rain and floor effects"""
        self.floor_splashes.draw(screen)
        self.raindrops.draw(screen)

# Example usage (for testing)
if __name__ == "__main__":
    clock = pygame.time.Clock()
    rain = Rain()

    running = True
    while running:
        screen.fill((30, 30, 30))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        rain.update(0, 0)  
        rain.draw(screen)

        pygame.display.flip()
        clock.tick(30)  

    pygame.quit()
