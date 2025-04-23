import pygame, random, sys, recipedata, os, Recipes, inventorydata  # type: ignore

class InteractionsUI:
    def __init__(self, game_instance):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.transparentSurface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("CUSTOMER INTERACTIONS")
        self.game = game_instance
        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.BRIGHT_BROWN = (143, 89, 68)
        self.BRIGHTEST_BROWN = (201, 125, 96)
        self.TRANSPARENT = (143, 89, 68, 0)

        # Fonts
        self.titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.buttonText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.dialougeText = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.headerText = pygame.font.Font(pygame.font.match_font('courier'), 48)
        self.bodyText = pygame.font.Font(pygame.font.match_font('courier'), 20)

        # State variables
        self.currentScene = "interior"  # Skip the first page by starting at "interior"
        self.previousScene = "NONE"
        self.waitingResponse = "I'm still waiting..."
        self.acceptedResponse = "Thanks! You've got talent."
        self.rejectedResponse = "That sucks. I'll head out."
        self.orderAccepted = False
        self.running = True
        self.closed = False

        self.randomCustomerNames = [
            "Taylor", "Riley", "Alex", "Rowan", "Ashton", "Parker",
            "Riley", "Charlie", "Aubrey", "Blake", "Phoenix", "Reagan"
        ] # gotta go gender neutral to simplify things i think
        random.shuffle(self.randomCustomerNames)
        self.nameIndex = 0

        self.mainButtons = {
            "Enter Shop": ("exterior", "interior", "PROBABLY_ILLEGAL_ASSETS/shop.png"),
            "Exit Shop": ("interior", "exterior", "PROBABLY_ILLEGAL_ASSETS/exit.png"),
            "View Customer Order": ("interior", "customerOrder", "PROBABLY_ILLEGAL_ASSETS/customer.png"),
            "Complete Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/complete.png"),
            "Close": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/exit.png"),
            "Reject Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/reject.png"),
            "Protagonist": ("interior", "", os.path.join(game_instance.SPRITE_PATH, game_instance.selected_character, "down_idle.png")),
            "Recipes": ("interior", "", "PROBABLY_ILLEGAL_ASSETS/recipe.png"),
        }
        self.renderedButtons = {}

        # Buttons
        self.menuButtons = {
            "QUIT": pygame.Rect(self.WIDTH // 2 - 150, 540, 80, 30),
            "Back to Garden": pygame.Rect(self.WIDTH // 2 - 20, 540, 200, 30)
        }

        self.listOfRecipes = list(recipedata.theRecipes.keys())
        self.currentOrder = random.choice(self.listOfRecipes)
        self.currentCustomerName = self.randomCustomerNames[self.nameIndex]
        print(f"currentOrder: {self.currentOrder}")
        print(f"currentCustomerName: {self.currentCustomerName}")

        self.generatedFakeAmounts = False
        self.notEnoughIngredients = False
        self.editedItemsAlready = False

        self.dialougeAnchorX = -60
        self.dialougeAnchorY = 275
        self.dialougeMaxWidth = 440
        self.dialougeMaxHeight = 110
        
        self.randomAmount = random.randint(100, 700)

    def center_x(self, width):
        """Return x coordinate to center an element with given width"""
        return (self.WIDTH - width) // 2
    
    def center_y(self, height):
        """Return y coordinate to center an element with given height"""
        return (self.HEIGHT - height) // 2

    def drawMainButton(self, name, xPos, yPos, buttonInformation):
        length = 300
        buttonRect = pygame.Rect(xPos // 2 + 60, yPos, length // 2, length // 2)
        if name == "Enter Shop":
            buttonRect = buttonRect.scale_by(2).move(185, 50)
        elif name == "Exit Shop":
            buttonRect = buttonRect.scale_by(.5).move(-125, -95)
        elif name == "View Customer Order":
            buttonRect = buttonRect.move((self.WIDTH - buttonRect.width) // 2 - (buttonRect.x), (self.HEIGHT // 2) - 40)
        elif name == "Complete Order" and not self.notEnoughIngredients:
            buttonRect = buttonRect.scale_by(.5)
            buttonRect.x = self.WIDTH - buttonRect.width - 50
            buttonRect.y = self.HEIGHT - buttonRect.height - 50
        elif name == "Reject Order":
            buttonRect = buttonRect.scale_by(.5)
            buttonRect.x = self.center_x(buttonRect.width)
            buttonRect.y = self.HEIGHT - buttonRect.height - 50
        elif name == "Close":
            buttonRect = buttonRect.scale_by(0.4)
            buttonRect.x = 50
            buttonRect.y = self.HEIGHT - buttonRect.height - 50
        elif name == "Protagonist":
            buttonRect = pygame.Rect(330, 150, 14 * 3, 29 * 3)
        elif name == "Recipes":
            buttonRect = pygame.Rect(self.WIDTH - 90, self.HEIGHT - 90, 64, 64)

        self.renderedButtons[name] = (buttonRect, buttonInformation[0], buttonInformation[1])

        if self.currentScene != buttonInformation[0]: return
        if name == "Complete Order" and self.notEnoughIngredients: return

        buttonImage = pygame.image.load(buttonInformation[2])
        buttonImage = pygame.transform.scale(buttonImage, (buttonRect.width, buttonRect.height))
        self.screen.blit(self.transparentSurface, (0, 0))
        pygame.draw.rect(self.transparentSurface, self.TRANSPARENT, buttonRect, border_radius=7)
        self.screen.blit(buttonImage, (buttonRect.x, buttonRect.y))

    def run(self):
        while self.running:
            if self.currentScene == "customerOrder":
                self.screen.fill(self.LIGHT_BROWN)
                middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
                shadow_offset = 6
                shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
                self.screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
                pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)

                panel_rect = pygame.Rect(80, 50, 645, 500)
                shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
                shadow_surface_inner.fill((0, 0, 0, 0))
                pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
                self.screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
                pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)
            else:
                self.screen.fill(self.WHITE)
                bg = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(self.currentScene) + ".png")
                bg = pygame.transform.scale(bg, (self.WIDTH, self.HEIGHT))
                self.screen.blit(bg, (0, 0))

            # Main Buttons
            xOffset = 300 - (len(self.mainButtons) * 25)
            yPosition = xOffset
            for name, info in self.mainButtons.items():
                self.drawMainButton(name, xOffset, yPosition, info)
                if self.currentScene == info[0] and name != "Exit Shop":
                    xOffset += 350

            showDialogue = self.currentScene == "interior" and self.previousScene == "customerOrder"
            if self.currentScene == "customerOrder":
                self.currentCustomerName = self.randomCustomerNames[self.nameIndex]

                # Header - centered properly
                headerLabel = self.headerText.render(self.currentOrder, True, self.WHITE)
                header_x = self.center_x(headerLabel.get_width())
                self.screen.blit(headerLabel, (header_x, 80))

                ingredients = recipedata.theRecipes.get(self.currentOrder)

                # Recipe image - positioned on left side
                recipeImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(self.currentOrder.replace(" ", "")) + ".png")
                recipeImage = pygame.transform.scale(recipeImage, (200, 200))
                recipe_x = 130
                recipe_y = self.center_y(200)
                self.screen.blit(recipeImage, (recipe_x, recipe_y))

                # Ensure bootlegIngredients is initialized before use
                if not self.generatedFakeAmounts:
                    bootlegIngredients = []
                    self.notEnoughIngredients = False
                    for i in range(len(ingredients)):
                        if not inventorydata.hasEnoughOfItem(ingredients[i]) and not self.notEnoughIngredients:
                            self.notEnoughIngredients = True
                            print(f"there was not enough of {ingredients[i]}")
                        bootlegIngredients.append((ingredients[i][0], inventorydata.quantityForItem(ingredients[i])))
                    self.generatedFakeAmounts = True
                else:
                    bootlegIngredients = []

                # Ingredients section - table layout
                ingredients_section_x = 380
                ingredients_section_y = 180
                
                # Ingredients header
                ingredients_header = self.bodyText.render("Ingredients:", True, self.WHITE)
                self.screen.blit(ingredients_header, (ingredients_section_x, ingredients_section_y))
                
                # Column headers
                need_x = ingredients_section_x + 180
                have_x = need_x + 80
                
                need_header = self.bodyText.render("Need", True, self.WHITE)
                have_header = self.bodyText.render("Have", True, self.WHITE)
                
                self.screen.blit(need_header, (need_x, ingredients_section_y + 30))
                self.screen.blit(have_header, (have_x, ingredients_section_y + 30))
                
                # Draw ingredients in rows
                row_height = 60
                img_size = 40
                
                for i, ingredient in enumerate(ingredients):
                    row_y = ingredients_section_y + 70 + (i * row_height)
                    
                    # Load and display ingredient image
                    try:
                        img_path = "PROBABLY_ILLEGAL_ASSETS/" + str.lower(ingredient[0]).replace(" ", "") + ".png"
                        ingredient_img = pygame.image.load(img_path)
                        ingredient_img = pygame.transform.scale(ingredient_img, (img_size, img_size))
                        self.screen.blit(ingredient_img, (ingredients_section_x, row_y))
                    except:
                        # Fallback if image not found
                        placeholder = self.bodyText.render("?", True, self.WHITE)
                        self.screen.blit(placeholder, (ingredients_section_x + 15, row_y + 10))
                    
                    # Ingredient name
                    name_label = self.bodyText.render(ingredient[0], True, self.WHITE)
                    self.screen.blit(name_label, (ingredients_section_x + img_size + 10, row_y + 10))
                    
                    # Need amount
                    need_amount = self.bodyText.render(str(ingredient[1]), True, self.WHITE)
                    self.screen.blit(need_amount, (need_x + 20, row_y + 10))
                    
                    # Have amount (from inventory, normalized name)
                    normalized_name = inventorydata.normalize_item_name(ingredient[0])
                    inventory_amount = inventorydata.quantityForItem((normalized_name, 0))
                    have_label = self.bodyText.render(str(inventory_amount), True, self.WHITE)
                    self.screen.blit(have_label, (have_x + 20, row_y + 10))

                # Accept and Reject buttons - positioned next to each other
                button_y = self.HEIGHT - 100  # Position near the bottom
                reject_button_x = self.WIDTH // 2 - 60  # Centered horizontally
                accept_button_x = reject_button_x + 120  # Positioned to the right of the reject button

                # Reject button
                reject_button = pygame.Rect(reject_button_x, button_y, 100, 40)
                pygame.draw.rect(self.screen, self.BRIGHT_BROWN, reject_button, border_radius=10)
                pygame.draw.rect(self.screen, self.DARK_BROWN, reject_button, 2, border_radius=10)
                reject_text = self.bodyText.render("Reject", True, self.WHITE)
                self.screen.blit(reject_text, reject_text.get_rect(center=reject_button.center))

                # Accept button (only if ingredients are sufficient)
                if not self.notEnoughIngredients:
                    accept_button = pygame.Rect(accept_button_x, button_y, 100, 40)
                    pygame.draw.rect(self.screen, (34, 139, 34), accept_button, border_radius=10)  # Green color
                    pygame.draw.rect(self.screen, self.DARK_BROWN, accept_button, 2, border_radius=10)
                    accept_text = self.bodyText.render("Accept", True, self.WHITE)
                    self.screen.blit(accept_text, accept_text.get_rect(center=accept_button.center))

                # Handle button clicks
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if reject_button.collidepoint(mouse_pos):
                            print("Order rejected!")
                            self.orderAccepted = False
                            self.closed = False
                            self.previousScene = self.currentScene
                            self.currentScene = "interior"
                        elif not self.notEnoughIngredients and accept_button.collidepoint(mouse_pos):
                            print("Order accepted!")
                            self.orderAccepted = True
                            self.closed = False
                            toDeduct = recipedata.theRecipes.get(self.currentOrder)
                            for i in range(len(toDeduct)):
                                fakeAmount = toDeduct[i][1] * -1
                                inventorydata.insertItemIntoSpareSlot((toDeduct[i][0], fakeAmount))
                            self.currentOrder = random.choice(self.listOfRecipes)
                            self.nameIndex += 1
                            if self.nameIndex > len(self.randomCustomerNames) - 1:
                                self.nameIndex = 0
                            random.shuffle(self.randomCustomerNames)
                            self.randomAmount = random.randint(100, 700)
                            self.generatedFakeAmounts = False
                            self.notEnoughIngredients = False
                            self.editedItemsAlready = False
                            self.previousScene = self.currentScene
                            self.currentScene = "interior"

            elif showDialogue:
                # Position the dialogue box in the top-right corner
                dialogue_width = self.dialougeMaxWidth
                dialogue_height = self.dialougeMaxHeight
                dialogue_x = self.WIDTH - dialogue_width - 20  # 20px padding from the right edge
                dialogue_y = 20  # 20px padding from the top
                
                # Draw dialogue box
                dialougeBrownRectPseudoOutline = pygame.Rect(dialogue_x, dialogue_y, dialogue_width, dialogue_height)
                pygame.draw.rect(self.screen, self.BROWN, dialougeBrownRectPseudoOutline, border_radius=5)
                
                # Inner white rectangle with consistent padding
                padding = 10
                dialougeWhiteRect = pygame.Rect(
                    dialogue_x + padding, 
                    dialogue_y + padding, 
                    dialogue_width - (padding * 2), 
                    dialogue_height - (padding * 2)
                )
                pygame.draw.rect(self.screen, self.WHITE, dialougeWhiteRect, border_radius=5)
                
                # Dialogue text
                text = self.currentCustomerName + ":\n\""
                if self.closed:
                    text = text + self.waitingResponse
                else:
                    text = text + (self.acceptedResponse if self.orderAccepted else self.rejectedResponse)
                text = text + "\""
                
                dialogueLabel = self.dialougeText.render(text, True, self.BROWN)
                text_x = dialogue_x + (padding * 2)
                text_y = dialogue_y + (padding * 2)
                self.screen.blit(dialogueLabel, (text_x, text_y))
                
                # Happy or Sad icon - positioned below the dialogue box
                iconImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/happy.png" if self.orderAccepted else "PROBABLY_ILLEGAL_ASSETS/sad.png")
                iconImage = pygame.transform.scale(iconImage, (40, 40))
                icon_x = dialogue_x + (dialogue_width - 40) // 2  # Centered below the dialogue box
                icon_y = dialogue_y + dialogue_height + 10  # 10px padding below the dialogue box
                self.screen.blit(iconImage, (icon_x, icon_y))

            # Event Handling
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for name, info in self.renderedButtons.items():
                        if not (info[0].collidepoint(mouse_pos) and self.currentScene == info[1]): continue
                        if name == "Recipes": Recipes.Recipes().run()
                        elif name == "Exit Shop":
                                print("Returning to game...")
                                self.running = False  # You can swap this to a callback to your Game instance
                                self.game.run()
                                break
                        elif info[2] != "":
                            print(f"{name} clicked! switching scene to {info[2]}")
                            self.closed = True
                            if name == "Reject Order" or name == "Complete Order":
                                if name == "Complete Order" and self.notEnoughIngredients:
                                    print(f"NOT ENOUGH INGREDIENTS. ABORT MISSION.")
                                    break
                                self.orderAccepted = name == "Complete Order"
                                self.closed = False
                                toDeduct = recipedata.theRecipes.get(self.currentOrder)
                                for i in range(len(toDeduct)):
                                    if not self.orderAccepted: break
                                    fakeAmount = toDeduct[i][1] * -1
                                    inventorydata.insertItemIntoSpareSlot((toDeduct[i][0], fakeAmount))
                                self.currentOrder = random.choice(self.listOfRecipes)
                                self.nameIndex += 1
                                if self.nameIndex > len(self.randomCustomerNames) - 1: self.nameIndex = 0
                                random.shuffle(self.randomCustomerNames)
                                self.randomAmount = random.randint(100, 700)
                                self.generatedFakeAmounts = False
                                self.notEnoughIngredients = False
                                self.editedItemsAlready = False
                            self.previousScene = self.currentScene
                            self.currentScene = info[2]
                            break

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = InteractionsUI()
    app.run()