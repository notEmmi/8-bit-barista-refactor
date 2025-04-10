import os
import pygame
import sys
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Player
player = pygame.Rect(100, 100, 50, 50)
player_speed = 5

# Blue tile (Fishing Spot)
fishing_tile = pygame.Rect(300, 100, 50, 50)

# Track the fish shown on the tile
current_tile_fish_index = random.randint(0, 2)

# Load fish images
fish_images = [
    pygame.transform.scale(pygame.image.load('fish_images/Orange.png').convert_alpha(), (25, 25)),
    pygame.transform.scale(pygame.image.load('fish_images/pink.png').convert_alpha(), (25, 25)),
    pygame.transform.scale(pygame.image.load('fish_images/Blue.png').convert_alpha(), (25, 25))
]
fish_data = [
    {"gold": 10, "slider_speed": 5},
    {"gold": 20, "slider_speed": 8},
    {"gold": 30, "slider_speed": 12}
]

# Minigame state
fishing_minigame = False
earned_gold = 0
current_fish = None

# Minigame UI setup
ui_rect = pygame.Rect(0, HEIGHT * 3 // 4, WIDTH, HEIGHT // 4)
green_target_width = 50
green_target = pygame.Rect(0, ui_rect.y + 20, green_target_width, ui_rect.height - 40)
white_slider = pygame.Rect(ui_rect.x, ui_rect.y + 20, 20, ui_rect.height - 40)
slider_direction = 1
slider_speed = 5  # Will update based on fish

# Shake effect
shake_offset = [0, 0]
shake_timer = 0

font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Player Movement
    if not fishing_minigame:
        if keys[pygame.K_w]: player.y -= player_speed
        if keys[pygame.K_s]: player.y += player_speed
        if keys[pygame.K_a]: player.x -= player_speed
        if keys[pygame.K_d]: player.x += player_speed

    # Interact with fishing spot
    if not fishing_minigame and keys[pygame.K_e] and player.colliderect(fishing_tile):
        fishing_minigame = True
        fish_index = current_tile_fish_index  # Use the same fish as the tile
        current_fish = fish_data[fish_index]
        slider_speed = current_fish["slider_speed"]
        green_target.x = random.randint(ui_rect.x + 50, ui_rect.right - green_target_width - 50)
        white_slider.x = ui_rect.x
        slider_direction = 1

    # Fishing minigame
    if fishing_minigame:
        white_slider.x += slider_speed * slider_direction
        if white_slider.right >= ui_rect.right or white_slider.left <= ui_rect.left:
            slider_direction *= -1

        if keys[pygame.K_SPACE]:
            if white_slider.colliderect(green_target):
                earned_gold += current_fish["gold"]
                fishing_minigame = False
                current_tile_fish_index = random.randint(0, 2)  # New fish on the tile!
            else:
                shake_timer = 10

    # Screen shake effect
    if shake_timer > 0:
        shake_offset[0] = random.randint(-5, 5)
        shake_offset[1] = random.randint(-5, 5)
        shake_timer -= 1
    else:
        shake_offset = [0, 0]

    # Drawing
    screen.fill((150, 200, 255))

    # Blue fishing tile with fish image
    pygame.draw.rect(screen, BLUE, fishing_tile)
    if not fishing_minigame:
        fish_img = fish_images[current_tile_fish_index]
        fish_x = fishing_tile.x + (fishing_tile.width // 2) - (fish_img.get_width() // 2)
        fish_y = fishing_tile.y + (fishing_tile.height // 2) - (fish_img.get_height() // 2)
        screen.blit(fish_img, (fish_x, fish_y))

    # Player
    pygame.draw.rect(screen, (255, 0, 0), player)

    # Fishing Minigame UI
    if fishing_minigame:
        pygame.draw.rect(screen, BLACK, ui_rect.move(shake_offset), border_radius=5)
        pygame.draw.rect(screen, GREEN, green_target.move(shake_offset))
        pygame.draw.rect(screen, WHITE, white_slider.move(shake_offset))
        # Draw current fish icon inside UI
        screen.blit(pygame.transform.scale(fish_images[fish_index], (50, 50)),
                    (WIDTH - 70, ui_rect.y + 10))

    # Gold counter
    gold_text = font.render(f'Gold: {earned_gold}', True, (0, 0, 0))
    screen.blit(gold_text, (10, 10))

    pygame.display.flip()

    # End the minigame after a successful catch or escape
    #if not fishing_minigame:
        #running = False  # Exit loop after fishing minigame ends

print(earned_gold)
sys.stdout.flush()
