# code reused from within the project from a branch by darren, permission granted in private --arthur
import pygame # type: ignore [this is so vscode doesn't yell at me]
import sys

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ADVANCED OPTIONS")

# Colors
LIGHT_BROWN = (99, 55, 44)  # Outer Background
DARK_BROWN = (38, 35, 34)  # Middle Dark Background
BROWN = (99, 55, 44)  # Inner Panel Color
WHITE = (255, 255, 255)
SHADOW_COLOR = (20, 20, 20, 30)
GRAY = (100, 100, 100)
ACTIVE_COLOR = (160, 100, 80)
BRIGHT_BROWN = (143, 89, 68)
BRIGHTEST_BROWN = (201, 125, 96)

# Fonts
titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
optionText = pygame.font.Font(pygame.font.match_font('courier'), 22)
inputValueText = pygame.font.Font(pygame.font.match_font('courier'), 18)

# Toggles
toggles = {
    "RAIN ANIMATIONS": True,
    "SHADERS": True,
    "SCREEN SHAKE": False,
}
toggleSquares = {}

# inputs
inputs = {
    "RANDOM SEED": 23457894738,
}
global inputRects
inputRects = {}

# Bottom menu buttons
menuButtons = {
    "BACK": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw a toggle
def drawToggle(name, yPos, value):
    min_x, max_x = 550, 590
    length = max_x - min_x
    buttonRect = pygame.Rect(min_x, yPos, length, length)
    toggleSquares[name] = (buttonRect, value)
    optionLabel = optionText.render(name, True, WHITE)
    screen.blit(optionLabel, (min_x // 2 - 50, yPos + 10))
    pygame.draw.rect(screen, BRIGHT_BROWN, buttonRect, border_radius=7)
    if (value != True): return
    buttonRectIfToggled = pygame.Rect(min_x + 5, yPos + 5, length - 10, length - 10)
    pygame.draw.rect(screen, BRIGHTEST_BROWN, buttonRectIfToggled, border_radius=7)

# Function to draw text input options
def drawTextInputs(name, yPos, value):
    min_x, max_x = 440, 590
    length, height = max_x - min_x, 40
    buttonRect = pygame.Rect(min_x, yPos, length, height)
    inputRects[name] = (buttonRect, value)
    optionLabel = optionText.render(name, True, WHITE)
    screen.blit(optionLabel, (min_x // 2 + 5, yPos + 10))
    pygame.draw.rect(screen, BRIGHT_BROWN, buttonRect, border_radius=7)
    inputValueLabel = inputValueText.render(str(value), True, WHITE)
    screen.blit(inputValueLabel, (min_x + 10, yPos + 10))

# Main Loop
running = True
while running:
    screen.fill(LIGHT_BROWN)  # Outer Coffee Background
    
    # Middle Dark Background
    middle_rect = pygame.Rect(30, 20, WIDTH - 60, HEIGHT - 40)
    shadow_offset = 6
    shadow_rect = middle_rect.move(shadow_offset, shadow_offset)
    shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 0))  # Fully transparent
    pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
    screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
    pygame.draw.rect(screen, DARK_BROWN, middle_rect, border_radius=12)
    
    # Inner Panel
    panel_rect = pygame.Rect(180, 50, 450, 500)
    shadow_rect_inner = panel_rect.move(shadow_offset, shadow_offset)
    shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
    pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
    screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
    pygame.draw.rect(screen, BROWN, panel_rect, border_radius=12)
    
    # Draw Title
    titleLabel = titleText.render("ADVANCED", True, WHITE)
    screen.blit(titleLabel, (WIDTH // 2 - titleLabel.get_width() // 2, 85))
    
    # Draw Sliders
    yOffset = 275 - (len(toggles) * 25) - 25 # -25 for seed text input height + padding
    for name, value in toggles.items():
        drawToggle(name, yOffset, value)
        yOffset += 60

    for inputName, inputValue in inputs.items():
        drawTextInputs(inputName, yOffset, inputValue)
        yOffset += 60

    # draw menuButtons
    for name, rect in menuButtons.items():
      pygame.draw.rect(screen, BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=14)
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))
    
    # Event Handling
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUITTING")
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("MOUSEDOWN")
            for name, rect in menuButtons.items():
                if not rect.collidepoint(mousePosition): continue
                print(f"{name} button clicked!")
                break
            for toggleName, rectAndValue in toggleSquares.items():
                if not rectAndValue[0].collidepoint(mousePosition): continue
                print(f"{toggleName} value before change: {toggles[toggleName]}")
                toggles[toggleName] = not toggles[toggleName]
                print(f"{toggleName} value after change: {toggles[toggleName]}")
                break
            for inputName, rectangleValueTuple in inputRects.items():
                if not rectangleValueTuple[0].collidepoint(mousePosition): continue
                print(f"{inputName} clicked. its value is {inputs[inputName]}")
                break
            x_positions = [320, 400, 480]
    
    pygame.display.flip()

pygame.quit()
sys.exit()