import pygame
import sys
class PetSelector:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pet Selector")

        # Set up clock for frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.WHITE = (255, 255, 255)

        self.background = pygame.image.load("images/petScreenBkgrnd.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))


        self.rightarrowRect = pygame.Rect(self.WIDTH -100, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        
        self.rightarrow = pygame.image.load("images/rightarrow.png")
        self.rightarrow = pygame.transform.scale(self.rightarrow, (50, 50))

        self.leftarrowRect = pygame.Rect( 100, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.leftarrow = pygame.image.load("images/leftarrow.png")
        self.leftarrow = pygame.transform.scale(self.leftarrow, (50, 50))
        

    def run(self):
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with white (or any color you like)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0,0))
            pygame.draw.rect(self.screen, self.WHITE, self.rightarrowRect)
            self.screen.blit(self.rightarrow, self.rightarrowRect.topleft) 

            pygame.draw.rect(self.screen, self.WHITE, self.leftarrowRect)
            self.screen.blit(self.leftarrow, self.leftarrowRect.topleft) # RGB color

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(self.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pet_selector = PetSelector()
    pet_selector.run()