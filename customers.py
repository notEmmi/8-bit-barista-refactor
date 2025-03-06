import pygame, random, sys, recipedata # type: ignore [this is so vscode doesn't yell at me]

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
transparentSurface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
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
TRANSPARENT = (143, 89, 68, 0)

# Fonts
titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
recipeNameText = pygame.font.Font(pygame.font.match_font('courier'), 22)
ingredientText = pygame.font.Font(pygame.font.match_font('courier'), 18)
buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
smallText = pygame.font.Font(pygame.font.match_font('courier'), 18)

renderedRecipes = {}

# Bottom menu buttons
menuButtons = {
    "BACK": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw a toggle
def drawRecipe(recipeName, xPos, yPos, ingredients):
    length = 125
    buttonRect = pygame.Rect(xPos, yPos, length, length)
    renderedRecipes[recipeName] = (buttonRect, recipedata.parseIngredients(ingredients))
    screen.blit(transparentSurface, (0, 0))
    pygame.draw.rect(transparentSurface, TRANSPARENT, buttonRect, border_radius=7)
    recipeImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(recipeName) + ".png")
    recipeImage = pygame.transform.scale(recipeImage, (length, length))
    screen.blit(recipeImage, (buttonRect.x, buttonRect.y))
    recipeLabel = recipeNameText.render(name, True, WHITE)
    screen.blit(recipeLabel, (xPos, yPos - recipeLabel.get_height() // 2))

# Main Loop
running = True
hasOrder = False
placedOrder = False
customersOrder = None
listOfRecipes = []
for recipe in recipedata.theRecipes.keys():
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
    screen.blit(titleLabel, (WIDTH // 2 - titleLabel.get_width() // 2, 72.5))
    
    # ingredient labels
    itemsPerRow = 3
    itemOnRow = 1
    xOffset = 300 - (len(recipedata.theRecipes) * 25)
    yOffset = 300 - (len(recipedata.theRecipes) * 25) + 10
    for name, ingredients in recipedata.theRecipes.items():
        drawRecipe(name, xOffset, yOffset, ingredients)
        xOffset += 190
        itemOnRow += 1
        if (itemOnRow > itemsPerRow):
            itemOnRow = 1
            xOffset = 300 - (len(recipedata.theRecipes) * 25)
            yOffset += 175

    # draw menuButtons
    for name, rect in menuButtons.items():
      pygame.draw.rect(screen, BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=14)
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
      pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
      text = buttonText.render(name, True, WHITE)
      screen.blit(text, text.get_rect(center=rect.center))

    if (not hasOrder):
        smallTextContents = ""
        hasOrder = random.randint(0,100) > 20
    if (hasOrder and not placedOrder):
        print("Order up!")
        randomRecipe = random.choice(listOfRecipes)
        customersOrder = renderedRecipes[randomRecipe]
        print(f"customer wants {randomRecipe}")
        placedOrder = True
        smallTextContents = "Customer wants " + randomRecipe + "."
    smallTextLabel = smallText.render(smallTextContents, True, WHITE)
    screen.blit(smallTextLabel, (WIDTH // 2 - smallTextLabel.get_width() // 2, 115))
    
    # Event Handling
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in menuButtons.items():
                if not rect.collidepoint(mousePosition): continue
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