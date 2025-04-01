# code reused from within the project from a branch by darren, permission granted in private --arthur
import pygame # type: ignore [this is so vscode doesn't yell at me]

class ControlsMenu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("KEYBINDS")

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)  # Outer Background
        self.DARK_BROWN = (38, 35, 34)  # Middle Dark Background
        self.BROWN = (99, 55, 44)  # Inner Panel Color
        self.WHITE = (255, 255, 255)
        self.SHADOW_COLOR = (20, 20, 20, 30)
        self.GRAY = (100, 100, 100)
        self.ACTIVE_COLOR = (160, 100, 80)
        self.BRIGHT_BROWN = (143, 89, 68)
        self.BRIGHTEST_BROWN = (201, 125, 96)

        # Fonts
        self.titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
        self.actionText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.keybindValueText = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # keybinds
        self.keybinds = {
            "MOVE UP": "W",
            "MOVE DOWN": "A",
            "MOVE LEFT": "S",
            "MOVE RIGHT": "D",
            "PRIMARY ACTION": "C",
            "SECONDARY ACTION": "X",
        }
        self.toggleSquares = {}

        # Bottom menu buttons
        self.menuButtons = {
            "BACK": pygame.Rect(self.WIDTH // 2 - 40, 485, 80, 30)
        }

        self.running = True

    # Function to draw a toggle
    def drawToggle(self, name, yPos, value):
        min_x, max_x = 550, 590
        length = max_x - min_x
        buttonRect = pygame.Rect(min_x, yPos, length, length)
        self.toggleSquares[name] = (buttonRect, value)
        actionLabel = self.actionText.render(name, True, self.WHITE)
        self.screen.blit(actionLabel, (min_x // 2 - 50, yPos + 10))
        pygame.draw.rect(self.screen, self.BRIGHT_BROWN, buttonRect, border_radius=7)
        keybindValueLabel = self.keybindValueText.render(value, True, self.WHITE)
        self.screen.blit(keybindValueLabel, (min_x + 15, yPos + 10))

    def run(self):
        # Main Loop
        while self.running:
            self.screen.fill(self.LIGHT_BROWN)  # Outer Coffee Background
            pygame.display.set_caption("KEYBINDS")
            
            # Middle Dark Background
            middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
            shadow_offset = 6
            shadow_rect = middle_rect.move(shadow_offset, shadow_offset)
            shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
            
            # Inner Panel
            panel_rect = pygame.Rect(180, 50, 450, 500)
            shadow_rect_inner = panel_rect.move(shadow_offset, shadow_offset)
            shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
            shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)
            
            # Draw Title
            titleLabel = self.titleText.render("KEYBINDS", True, self.WHITE)
            self.screen.blit(titleLabel, (self.WIDTH // 2 - titleLabel.get_width() // 2, 85))
            
            # Draw Sliders
            yOffset = 300 - (len(self.keybinds) * 25)
            for name, value in self.keybinds.items():
                self.drawToggle(name, yOffset, value)
                yOffset += 50

            # draw menuButtons
            for name, rect in self.menuButtons.items():
                pygame.draw.rect(self.screen, self.BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=14)
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))
            
            # Event Handling
            mousePosition = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITTING")
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("MOUSEDOWN")
                    for name, rect in self.menuButtons.items():
                        if not rect.collidepoint(mousePosition): continue
                        return "options"
                    for actionName, rectAndValue in self.toggleSquares.items():
                        if not rectAndValue[0].collidepoint(mousePosition): continue
                        print(f"{actionName} clicked. keybind: {self.keybinds[actionName]}")
            
            pygame.display.flip()