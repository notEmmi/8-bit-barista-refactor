import pygame
import sys

# Initialize Pygame
pygame.init()

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (32, 32, 32)
TEXT_COLOR = (255, 255, 255)

class LoadingScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Loading Screen")
        self.font = pygame.font.Font(None, 74)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BACKGROUND_COLOR)
            loading_text = self.font.render("Loading...", True, TEXT_COLOR)
            text_rect = loading_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(loading_text, text_rect)
            
            pygame.display.flip()

if __name__ == "__main__":
    loading_screen = LoadingScreen()
    loading_screen.run()
