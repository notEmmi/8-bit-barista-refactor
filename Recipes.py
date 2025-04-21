import pygame
import Popular
import settingsdata
from pygame import mixer

class Recipes:
    def __init__(self,path_back_to_cafe):
        # Initialize pygame
        pygame.init()
        mixer.init()

        self.pathbacktocafe = path_back_to_cafe 

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recipes")
        
        # Load images
        self.recipes = pygame.image.load("images/recipes.png")
        self.recipes = pygame.transform.scale(self.recipes, (350, 150))
        
        self.kitchen = pygame.image.load("images/kitchen.png")
        self.kitchen = pygame.transform.scale(self.kitchen, (self.WIDTH, self.HEIGHT))
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.LIGHTBROWN = (254, 195, 117)
        self.BACKGROUNDBROWN = (205, 149, 74)
        self.SADDLEBROWN = (139, 69, 19)
        self.BLACK = (0, 0, 0)

        # Rectangle dimensions
        self.RECT_WIDTH, self.RECT_HEIGHT = 200, 100
        self.SPACING = 20
        
        # Calculate center positions
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2
        
        # Define rectangles
        self.topLeftRect = pygame.Rect(center_x - self.RECT_WIDTH - self.SPACING // 2, center_y - self.RECT_HEIGHT - self.SPACING // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.topRightRect = pygame.Rect(center_x + self.SPACING // 2, center_y - self.RECT_HEIGHT - self.SPACING // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.bottomLeftRect = pygame.Rect(center_x - self.RECT_WIDTH - self.SPACING // 2, center_y + self.SPACING // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        self.bottomRightRect = pygame.Rect(center_x + self.SPACING // 2, center_y + self.SPACING // 2, self.RECT_WIDTH, self.RECT_HEIGHT)
        
        # Create surfaces for rectangles
        self.topLeftRect_Surface = pygame.Surface((self.RECT_WIDTH, self.RECT_HEIGHT))
        self.topLeftRect_Surface.fill(self.LIGHTBROWN)
        self.topRightRect_Surface = pygame.Surface((self.RECT_WIDTH, self.RECT_HEIGHT))
        self.topRightRect_Surface.fill(self.LIGHTBROWN)
        self.bottomLeftRect_Surface = pygame.Surface((self.RECT_WIDTH, self.RECT_HEIGHT))
        self.bottomLeftRect_Surface.fill(self.LIGHTBROWN)
        self.bottomRightRect_Surface = pygame.Surface((self.RECT_WIDTH, self.RECT_HEIGHT))
        self.bottomRightRect_Surface.fill(self.LIGHTBROWN)


        self.backButton = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 60, 200, 40)
        
        # Load font
        self.font = pygame.font.Font(pygame.font.match_font("courier"), 24)
        
        # Load and play background music
        mixer.music.load("tracks/08 - Shop.mp3")
        mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
        mixer.music.play()
        
    def draw_text(self, surface, text, rect, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect.topleft)
    
    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Check for hover effect
                if self.topLeftRect.collidepoint(mouse_pos):
                    self.topLeftRect_Surface.fill(self.SADDLEBROWN)
                elif self.topRightRect.collidepoint(mouse_pos):
                    self.topRightRect_Surface.fill(self.SADDLEBROWN)
                elif self.bottomLeftRect.collidepoint(mouse_pos):
                    self.bottomLeftRect_Surface.fill(self.SADDLEBROWN)
                elif self.bottomRightRect.collidepoint(mouse_pos):
                    self.bottomRightRect_Surface.fill(self.SADDLEBROWN)
                else:
                    self.topLeftRect_Surface.fill(self.LIGHTBROWN)
                    self.topRightRect_Surface.fill(self.LIGHTBROWN)
                    self.bottomLeftRect_Surface.fill(self.LIGHTBROWN)
                    self.bottomRightRect_Surface.fill(self.LIGHTBROWN)
                
                # Check for click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.topLeftRect.collidepoint(event.pos):
                        Popular.runPopular()
                        running = False
                
                    if self.backButton.collidepoint(event.pos):
                      print("Returning to cafe...")
                      running = False
                      self.pathbacktocafe.run()
            # Draw background and UI elements
            self.screen.blit(self.kitchen, (0, 0))
            self.screen.blit(self.recipes, (225, 25))
            self.screen.blit(self.topLeftRect_Surface, self.topLeftRect.topleft)
            self.screen.blit(self.topRightRect_Surface, self.topRightRect.topleft)
            self.screen.blit(self.bottomLeftRect_Surface, self.bottomLeftRect.topleft)
            self.screen.blit(self.bottomRightRect_Surface, self.bottomRightRect.topleft)
            
            # Draw text on rectangles
            self.draw_text(self.screen, "Popular", self.topLeftRect, self.font, self.BLACK)
            self.draw_text(self.screen, "Coffee", self.topRightRect, self.font, self.BLACK)
            self.draw_text(self.screen, "Tea", self.bottomLeftRect, self.font, self.BLACK)
            self.draw_text(self.screen, "Desserts", self.bottomRightRect, self.font, self.BLACK)
            pygame.draw.rect(self.screen, self.SADDLEBROWN, self.backButton.inflate(4, 4), border_radius=12)
            pygame.draw.rect(self.screen, self.LIGHTBROWN, self.backButton, border_radius=12)
            self.draw_text(self.screen, "Back to Game", self.backButton, self.font, self.BLACK)
            
            pygame.display.flip()
        
        pygame.quit()

# Create an instance of RecipeScreen and run it
if __name__ == "__main__":
     app = Recipes()
     app.run()

