import pygame, random, sys, recipedata # type: ignore [this is so vscode doesn't yell at me]

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CUSTOMER INTERACTIONS")

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
buttonText = pygame.font.Font(pygame.font.match_font('courier'), 22)
recipeText = pygame.font.Font(pygame.font.match_font('courier'), 32)
ingredientText = pygame.font.Font(pygame.font.match_font('courier'), 18)

currentScene = "exterior"

# items
mainButtons = {
    "Enter Shop": ("exterior", "interior"),
    "View Customer Order": ("interior", "customerOrder"),
    "Exit Shop": ("interior", "exterior"),
    "Complete Order": ("customerOrder", "interior"),
    "Reject Order": ("customerOrder", "interior"),
    "Close": ("customerOrder", "interior"),
}
renderedButtons = {}

# Bottom menu buttons
menuButtons = {
    "QUIT": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw a main button
def drawMainButton(name, yPos, intendedSceneAndNextScene):
    min_x, max_x = 350, 590
    length = max_x - min_x
    buttonRect = pygame.Rect(min_x // 2 - 60, yPos + 2.5, length * 2.4, 40)
    renderedButtons[name] = (buttonRect, intendedSceneAndNextScene[0], intendedSceneAndNextScene[1])
    if (currentScene != intendedSceneAndNextScene[0]): return
    pygame.draw.rect(screen, BRIGHT_BROWN, buttonRect, border_radius=7)
    buttonLabel = buttonText.render(name, True, WHITE)
    screen.blit(buttonLabel, (min_x // 2 - 50, yPos + 10))

# Main Loop
running = True
listOfRecipes = []
for recipe in recipedata.theRecipes.keys():
    listOfRecipes.append(recipe)
currentOrder = random.choice(listOfRecipes)
print(f"currentOrder: {currentOrder}")
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
    panel_rect = pygame.Rect(80, 50, 645, 500)
    shadow_rect_inner = panel_rect.move(shadow_offset, shadow_offset)
    shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
    pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
    screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
    pygame.draw.rect(screen, BROWN, panel_rect, border_radius=12)
    
    # Draw Title
    titleLabel = titleText.render(currentScene, True, WHITE)
    screen.blit(titleLabel, (WIDTH // 2 - titleLabel.get_width() // 2, 85))
    
    # ingredient labels
    yOffset = 300 - (len(mainButtons) * 25)
    for name, intendedSceneAndNextScene in mainButtons.items():
        drawMainButton(name, yOffset, intendedSceneAndNextScene)
        if (currentScene == intendedSceneAndNextScene[0]): yOffset += 50

    # draw menuButtons
    for name, rect in menuButtons.items():
      pygame.draw.rect(screen, BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=14)
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))

    if (currentScene == "customerOrder"):
        recipeLabel = recipeText.render(currentOrder, True, WHITE)
        screen.blit(recipeLabel, (WIDTH // 2 - recipeLabel.get_width() // 2, HEIGHT // 2 + 40))
        ingredientLabel = ingredientText.render(recipedata.parseIngredients(recipedata.theRecipes.get(currentOrder)), True, WHITE)
        screen.blit(ingredientLabel, (WIDTH // 2 - ingredientLabel.get_width() // 2, HEIGHT // 2 + 80))
    
    # Event Handling
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUITTING")
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("MOUSEDOWN")
            for menuButtonName, rect in menuButtons.items():
                if not rect.collidepoint(mousePosition): continue
                print(f"{menuButtonName} button clicked!")
                if (menuButtonName == "QUIT"): running = False
                break
            for mainButtonName, buttonIntendedNext in renderedButtons.items():
                if not buttonIntendedNext[0].collidepoint(mousePosition) or currentScene != buttonIntendedNext[1]: continue
                print(f"{mainButtonName} clicked! switching scene to {buttonIntendedNext[2]}")
                if (mainButtonName == "Reject Order"):
                    print(f"rejected order {currentOrder}. customer could express disappointment here. generating new order...")
                    currentOrder = random.choice(listOfRecipes)
                    print(f"new order: {currentOrder}")
                elif (mainButtonName == "Complete Order"):
                    print(f"Completed order {currentOrder}. customer expresses appreciation here. generating new order...")
                    currentOrder = random.choice(listOfRecipes)
                    print(f"new order: {currentOrder}")
                currentScene = buttonIntendedNext[2]
                break
            x_positions = [320, 400, 480]
    
    pygame.display.flip()

pygame.quit()
sys.exit()