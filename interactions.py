import pygame, random, sys, recipedata  # type: ignore

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
        self.headerText = pygame.font.Font(pygame.font.match_font('courier'), 32)
        self.bodyText = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # State variables
        self.currentScene = "interior"  # Skip the first page by starting at "interior"
        self.previousScene = "NONE"
        self.waitingResponse = "I'm still waiting..."
        self.acceptedResponse = "Thanks!"
        self.rejectedResponse = "That sucks."
        self.orderAccepted = False
        self.running = True
        self.closed = False

        self.mainButtons = {
            "Enter Shop": ("exterior", "interior", "PROBABLY_ILLEGAL_ASSETS/shop.png"),
            # "Exit Shop": ("interior", "exterior", "PROBABLY_ILLEGAL_ASSETS/exit.png"),  # Commented out
            "View Customer Order": ("interior", "customerOrder", "PROBABLY_ILLEGAL_ASSETS/customer.png"),
            "Complete Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/complete.png"),
            "Close": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/close.png"),
            "Reject Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/reject.png"),
        }
        self.renderedButtons = {}

        # Buttons
        self.menuButtons = {
            "QUIT": pygame.Rect(self.WIDTH // 2 - 120, 540, 80, 30),
            "Return To Game": pygame.Rect(self.WIDTH // 2 + 40, 540, 160, 30)
        }

        self.listOfRecipes = list(recipedata.theRecipes.keys())
        self.currentOrder = random.choice(self.listOfRecipes)
        print(f"currentOrder: {self.currentOrder}")

    def drawMainButton(self, name, xPos, yPos, buttonInformation):
        length = 300
        buttonRect = pygame.Rect(xPos // 2 + 60, yPos, length // 2, length // 2)
        # if name == "Exit Shop":  # Commented out
        #     buttonRect = buttonRect.scale_by(0.3).move(-85, -110)
        if name == "Enter Shop":
            buttonRect = buttonRect.scale_by(2).move(185, 50)
        elif name == "View Customer Order":
            buttonRect = buttonRect.move(self.WIDTH // 2 - buttonRect.width // 2 - buttonRect.x, 0)  # Center horizontally
        elif name == "Complete Order":
            buttonRect = buttonRect.move(75, 25)
        elif name == "Reject Order":
            buttonRect = buttonRect.move(-45, 25)
        elif name == "Close":
            buttonRect = buttonRect.scale_by(0.4).move(-250, -115)

        self.renderedButtons[name] = (buttonRect, buttonInformation[0], buttonInformation[1])

        if self.currentScene != buttonInformation[0]:
            return

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
                if self.currentScene == info[0]:
                    xOffset += 350

            showDialogue = self.currentScene == "interior" and self.previousScene == "customerOrder"
            if self.currentScene == "customerOrder":
                headerLabel = self.headerText.render(self.currentOrder, True, self.WHITE)
                self.screen.blit(headerLabel, (self.WIDTH // 2 - headerLabel.get_width() // 2, self.HEIGHT // 2 + 100))
                bodyLabel = self.bodyText.render(recipedata.parseIngredients(recipedata.theRecipes.get(self.currentOrder)), True, self.WHITE)
                self.screen.blit(bodyLabel, (self.WIDTH // 2 - bodyLabel.get_width() // 2, self.HEIGHT // 2 + 140))
                recipeImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(self.currentOrder) + ".png")
                recipeImage = pygame.transform.scale(recipeImage, (recipeImage.get_width() // 2, recipeImage.get_height() // 2))
                self.screen.blit(recipeImage, (self.WIDTH // 2 - recipeImage.get_width() // 2, 285))
            elif showDialogue:
                if self.closed:
                    text = self.waitingResponse
                else:
                    text = self.acceptedResponse if self.orderAccepted else self.rejectedResponse
                dialogueLabel = self.headerText.render(text, True, self.WHITE)
                self.screen.blit(dialogueLabel, (self.WIDTH // 2 - dialogueLabel.get_width() // 2, self.HEIGHT // 2 + 150))

            for name, rect in self.menuButtons.items():
                pygame.draw.rect(self.screen, self.BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=14)
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))

            # Event Handling
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for name, rect in self.menuButtons.items():
                        if rect.collidepoint(mouse_pos):
                            if name == "QUIT":
                                self.running = False
                            elif name == "Return To Game":
                                print("Returning to game...")
                                self.running = False  # You can swap this to a callback to your Game instance
                                self.game.run()
                            break
                    for name, info in self.renderedButtons.items():
                        if info[0].collidepoint(mouse_pos) and self.currentScene == info[1]:
                            print(f"{name} clicked! switching scene to {info[2]}")
                            self.closed = True
                            if name == "Reject Order":
                                self.orderAccepted = False
                                self.closed = False
                                self.currentOrder = random.choice(self.listOfRecipes)
                            elif name == "Complete Order":
                                self.orderAccepted = True
                                self.closed = False
                                self.currentOrder = random.choice(self.listOfRecipes)
                            self.previousScene = self.currentScene
                            self.currentScene = info[2]
                            break

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = InteractionsUI()
    app.run()
