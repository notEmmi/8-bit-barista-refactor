import pygame
import Unlock
import settingsdata
from pygame import mixer

class Popular:
    def __init__(self, return_to_recipes_instance):
        self.return_to_recipes = return_to_recipes_instance
        pygame.init()
        mixer.init()

        # Screen setup
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Popular")

        # Colors
        self.WHITE = (255, 255, 255)
        self.LIGHTBROWN = (254, 195, 117)
        self.BACKGROUNDBROWN = (205, 149, 74)
        self.SADDLEBROWN = (139, 69, 19)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)

        # Load images
        self.kitchen = pygame.transform.scale(pygame.image.load("images/kitchen.png"), (self.WIDTH, self.HEIGHT))
        self.bagel = pygame.transform.scale(pygame.image.load("images/bagel.png"), (100, 50))
        self.coffee = pygame.transform.scale(pygame.image.load("images/coffee.png"), (100, 50))
        self.croissant = pygame.transform.scale(pygame.image.load("images/croisant.png"), (100, 50))
        self.lock = pygame.transform.scale(pygame.image.load("images/lock.png"), (100, 50))
        self.popup = pygame.transform.scale(pygame.image.load("images/popup.png"), (75, 75))
        self.exclaimationPoint = pygame.transform.scale(pygame.image.load("images/exPoint.png"), (30, 30))

        # Font
        self.font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 24)
        self.popularFont = pygame.font.Font(pygame.font.match_font("Irish Grover"), 48)

        # Rectangles
        self.setup_rectangles()

        # Music
        mixer.music.load("tracks/08 - Shop.mp3")
        mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
        mixer.music.play()

    def setup_rectangles(self):
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
        self.RECT_WIDTH, self.RECT_HEIGHT = 200, 100
        spacing = 20

        self.popularTextRect = pygame.Rect(center_x - 150, center_y - 225, 300, 100)
        self.topLeftRect = pygame.Rect(center_x - self.RECT_WIDTH - spacing // 2, center_y - self.RECT_HEIGHT - spacing // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.topRightRect = pygame.Rect(center_x + spacing // 2, center_y - self.RECT_HEIGHT - spacing // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.bottomLeftRect = pygame.Rect(center_x - self.RECT_WIDTH - spacing // 2, center_y + spacing // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.bottomRightRect = pygame.Rect(center_x + spacing // 2, center_y + spacing // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        
        
        self.backButton = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 60, 200, 40)


    def draw_text(self, surface, text, rect, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect.topleft)

    def draw_button_with_depth(self, surface, rect, color, shadow_offset=4, shadow_alpha=100):
    # Draw shadow
     shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
     shadow.fill((0, 0, 0, 0))
     pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha), shadow.get_rect(), border_radius=10)
     surface.blit(shadow, (rect.x + shadow_offset, rect.y + shadow_offset))

    # Draw button on top
     pygame.draw.rect(surface, color, rect, border_radius=10)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bottomRightRect.collidepoint(event.pos):
                        Unlock.runUnlock()
                        running = False

                    if self.backButton.collidepoint(event.pos):
                     print("Returning to Recipes...")
                     running = False
                     self.return_to_recipes.run()

                

            # Highlight logic
            topLeftColor = self.SADDLEBROWN if self.topLeftRect.collidepoint(mouse_pos) else self.LIGHTBROWN
            topRightColor = self.SADDLEBROWN if self.topRightRect.collidepoint(mouse_pos) else self.LIGHTBROWN
            bottomLeftColor = self.SADDLEBROWN if self.bottomLeftRect.collidepoint(mouse_pos) else self.LIGHTBROWN
            bottomRightColor = self.BLUE if self.bottomRightRect.collidepoint(mouse_pos) else self.LIGHTBROWN

            # Draw background
            self.screen.blit(self.kitchen, (0, 0))

            # Draw rectangles and images
            self.draw_button_with_depth(self.screen, self.topLeftRect, topLeftColor)
            self.draw_button_with_depth(self.screen, self.topRightRect, topRightColor)
            self.draw_button_with_depth(self.screen, self.bottomLeftRect, bottomLeftColor)
            self.draw_button_with_depth(self.screen, self.bottomRightRect, bottomRightColor)
            self.draw_button_with_depth(self.screen, self.popularTextRect, self.LIGHTBROWN)
            self.screen.blit(self.bagel, self.bagel.get_rect(center=self.topLeftRect.center))
            self.screen.blit(self.coffee, self.coffee.get_rect(center=self.topRightRect.center))
            self.screen.blit(self.croissant, self.croissant.get_rect(center=self.bottomLeftRect.center))
            self.screen.blit(self.lock, self.lock.get_rect(center=self.bottomRightRect.center))

            # Draw popup if hovering bottom right
            if self.bottomRightRect.collidepoint(mouse_pos):
                self.screen.blit(self.popup, (425, 250))

            # Text and icons
            self.draw_text(self.screen, "Popular", self.popularTextRect, self.popularFont, self.BLACK)
            self.screen.blit(self.exclaimationPoint, self.bottomRightRect.topleft)

            pygame.draw.rect(self.screen, self.SADDLEBROWN, self.backButton.inflate(4, 4), border_radius=12)
            pygame.draw.rect(self.screen, self.LIGHTBROWN, self.backButton, border_radius=12)
            self.draw_text(self.screen, "Back to Recipes", self.backButton, self.font, self.BLACK)

            pygame.display.flip()

        pygame.quit()
