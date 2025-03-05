import pygame, random, sys, recipedata # type: ignore [this is so vscode doesn't yell at me]

# Initialize Pygame
pygame.init()

# Screen Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
transparentSurface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
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
TRANSPARENT = (143, 89, 68, 0)

# Fonts
titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
buttonText = pygame.font.Font(pygame.font.match_font('courier'), 22)
headerText = pygame.font.Font(pygame.font.match_font('courier'), 32)
bodyText = pygame.font.Font(pygame.font.match_font('courier'), 18)

currentScene = "exterior"
previousScene = "NONE"

waitingResponse = "I'm still waiting..."
acceptedResponse = "Thanks!"
rejectedResponse = "That sucks."
orderAccepted = False

# items
mainButtons = {
    "Enter Shop": ("exterior", "interior", "PROBABLY_ILLEGAL_ASSETS/shop.png"),
    "Exit Shop": ("interior", "exterior", "PROBABLY_ILLEGAL_ASSETS/exit.png"),
    "View Customer Order": ("interior", "customerOrder", "PROBABLY_ILLEGAL_ASSETS/customer.png"),
    "Complete Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/complete.png"),
    "Close": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/close.png"),
    "Reject Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/reject.png"),
}
renderedButtons = {}

# Bottom menu buttons
menuButtons = {
    "QUIT": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30)
}

# Function to draw a main button
def drawMainButton(name, xPos, yPos, buttonInformation):
    length = 300
    buttonRect = pygame.Rect(xPos // 2 + 60, yPos, length // 2, length // 2)
    if (name == "Exit Shop"):
        buttonRect = buttonRect.scale_by(0.3)
        buttonRect = buttonRect.move(-85, -110)
    elif (name == "Enter Shop"):
        buttonRect = buttonRect.scale_by(2)
        buttonRect = buttonRect.move(185, 50)
    elif (name == "Complete Order"):
        buttonRect = buttonRect.move(75, 25)
    elif (name == "Reject Order"):
        buttonRect = buttonRect.move(-45, 25)
    elif (name == "Close"):
        buttonRect = buttonRect.scale_by(.4)
        buttonRect = buttonRect.move(-250, -115)
    renderedButtons[name] = (buttonRect, buttonInformation[0], buttonInformation[1])
    if (currentScene != buttonInformation[0]): return
    buttonImage = pygame.image.load(buttonInformation[2])
    buttonImage = pygame.transform.scale(buttonImage, (buttonRect.width, buttonRect.height))
    screen.blit(transparentSurface, (0, 0))
    pygame.draw.rect(transparentSurface, TRANSPARENT, buttonRect, border_radius=7)
    screen.blit(buttonImage, (buttonRect.x, buttonRect.y))

# Main Loop
running = True
closed = False
listOfRecipes = []
for recipe in recipedata.theRecipes.keys():
    listOfRecipes.append(recipe)
currentOrder = random.choice(listOfRecipes)
print(f"currentOrder: {currentOrder}")
while running:
    if (currentScene == "customerOrder"):
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
    else:
        screen.fill(WHITE)  # Outer Coffee Background
        backgroundImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(currentScene) + ".png")
        backgroundImage = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))
        screen.blit(backgroundImage, (0,0))
    
    # buttons
    xOffset = 300 - (len(mainButtons) * 25)
    yPosition = xOffset
    for name, buttonInformation in mainButtons.items():
        drawMainButton(name, xOffset, yPosition, buttonInformation)
        if (currentScene == buttonInformation[0]): xOffset += 350

    showDialouge = currentScene == "interior" and previousScene == "customerOrder"
    if (currentScene == "customerOrder"):
        headerLabel = headerText.render(currentOrder, True, WHITE)
        screen.blit(headerLabel, (WIDTH // 2 - headerLabel.get_width() // 2, HEIGHT // 2 + 100))
        bodyLabel = bodyText.render(recipedata.parseIngredients(recipedata.theRecipes.get(currentOrder)), True, WHITE)
        screen.blit(bodyLabel, (WIDTH // 2 - bodyLabel.get_width() // 2, HEIGHT // 2 + 140))
        imagePath = "PROBABLY_ILLEGAL_ASSETS/" + str.lower(currentOrder) + ".png"
        recipeImage = pygame.image.load(imagePath)
        recipeImage = pygame.transform.scale(recipeImage, (recipeImage.get_width() // 2, recipeImage.get_height() // 2))
        screen.blit(recipeImage, (WIDTH // 2 - recipeImage.get_width() // 2, 285))
    elif (showDialouge):
        if (closed):
            text = waitingResponse
        else:
            if (orderAccepted): text = acceptedResponse
            else: text = rejectedResponse
        headerLabel = headerText.render(text, True, WHITE)
        screen.blit(headerLabel, (WIDTH // 2 - headerLabel.get_width() // 2, HEIGHT // 2 + 150))

    
    # Event Handling
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for menuButtonName, rect in menuButtons.items():
                if not rect.collidepoint(mousePosition): continue
                if (menuButtonName == "QUIT"): running = False
                break
            for mainButtonName, buttonIntendedNext in renderedButtons.items():
                if not buttonIntendedNext[0].collidepoint(mousePosition) or currentScene != buttonIntendedNext[1]: continue
                print(f"{mainButtonName} clicked! switching scene to {buttonIntendedNext[2]}")
                closed = True
                if (mainButtonName == "Reject Order"):
                    orderAccepted = False
                    closed = False
                    print(f"rejected order {currentOrder}. customer could express disappointment here. generating new order...")
                    currentOrder = random.choice(listOfRecipes)
                    print(f"new order: {currentOrder}")
                elif (mainButtonName == "Complete Order"):
                    orderAccepted = True
                    closed = False
                    print(f"Completed order {currentOrder}. customer expresses appreciation here. generating new order...")
                    currentOrder = random.choice(listOfRecipes)
                    print(f"new order: {currentOrder}")
                previousScene = currentScene
                currentScene = buttonIntendedNext[2]
                break
            x_positions = [320, 400, 480]
    
    pygame.display.flip()

pygame.quit()
sys.exit()