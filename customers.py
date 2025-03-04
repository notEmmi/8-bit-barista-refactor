import pygame, random, sys # type: ignore [this is so vscode doesn't yell at me]

"""
This one python file is meant to complete both task cards #63 and #73.
This is a barebones crafting menu right now.
It will be linked with code from other branches to minimize code duplication.
Right now it has a gameloop with 80% chance of calling a customer to "simulate" coffeeshop customer flow.
"""

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ORDER FULFILLMENT")

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
recipeNameText = pygame.font.Font(pygame.font.match_font('courier'), 22)
ingredientText = pygame.font.Font(pygame.font.match_font('courier'), 18)
buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)

# items
theRecipes = {
    "Bagel": [("Wheat", 3)],
    "Croissant": [("Wheat", 2), ("Butter", 1)],
    "Muffin": [("Wheat", 3), ("Sugar", 3), ("Milk", 1)],
    "Coffee": [("Beans", 4), ("Milk", 1), ("Sugar", 1), ("Cream", 1)],
    "Tea": [("Water", 1), ("Tea Leaves", 3)],
    "Smoothie": [("Water", 1), ("Banana", 1), ("Melon", 2)],
}
renderedRecipes = {}

# Bottom menu buttons
menuButtons = {
    "BACK": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw a toggle
def drawRecipe(name, yPos, ingredients):
    min_x, max_x = 350, 590
    length = max_x - min_x
    buttonRect = pygame.Rect(min_x // 2 - 60, yPos + 2.5, length * 2.4, 40)
    pygame.draw.rect(screen, BRIGHT_BROWN, buttonRect, border_radius=7)
    ingredientString = ""
    for ingredientAndAmount in ingredients:
        ingredientString = ingredientString + " " + str(ingredientAndAmount[1]) + " " + ingredientAndAmount[0] + ","
    if (len(ingredientString) > 1): ingredientString = ingredientString[:-1] # remove trailing comma
    recipeLabel = recipeNameText.render((name + ":" + str(ingredientString)), True, WHITE)
    screen.blit(recipeLabel, (min_x // 2 - 50, yPos + 10))
    renderedRecipes[name] = (buttonRect, ingredientString)

# Main Loop
running = True
hasOrder = False
placedOrder = False
customersOrder = None
listOfRecipes = []
for recipe in theRecipes.keys():
    listOfRecipes.append(recipe)
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
    titleLabel = titleText.render("ORDER FULFILLMENT", True, WHITE)
    screen.blit(titleLabel, (WIDTH // 2 - titleLabel.get_width() // 2, 85))
    
    # ingredient labels
    yOffset = 300 - (len(theRecipes) * 25)
    for name, ingredients in theRecipes.items():
        drawRecipe(name, yOffset, ingredients)
        yOffset += 50

    # draw menuButtons
    for name, rect in menuButtons.items():
      pygame.draw.rect(screen, BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=14)
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))

    if (not hasOrder): hasOrder = random.randint(0,100) > 20
    if (hasOrder and not placedOrder):
        print("Order up!")
        randomRecipe = random.choice(listOfRecipes)
        customersOrder = renderedRecipes[randomRecipe]
        print(f"customer wants {randomRecipe}")
        placedOrder = True
    
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
            for recipe, buttonAndIngredients in renderedRecipes.items():
                if not buttonAndIngredients[0].collidepoint(mousePosition): continue
                print(f"User wants to craft {recipe}, and needs\n\t{buttonAndIngredients[1]}.")
                if (placedOrder and customersOrder == buttonAndIngredients):
                    print("order fulfilled!")
                    hasOrder = False
                    placedOrder = False
                else:
                    print(f"{recipe} is not what the customer ordered.")
                break
            x_positions = [320, 400, 480]
    
    pygame.display.flip()

pygame.quit()
sys.exit()