import pygame
import sys
class PetSelector:
    def __init__(self): ## pass a pet type that will be used to decide between lists of pngs to choose from
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


        self.rightarrowRect = pygame.Rect(self.WIDTH -150, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.rightArrowsurface = pygame.Surface((self.rightarrowRect.width, self.rightarrowRect.height))
        self.rightarrow = pygame.image.load("images/rightarrow.png")
        self.rightarrow = pygame.transform.scale(self.rightarrow, (50, 50))

        self.leftarrowRect = pygame.Rect((self.WIDTH-self.WIDTH)+100, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.leftarrow = pygame.image.load("images/leftarrow.png")
        self.leftarrow = pygame.transform.scale(self.leftarrow, (50, 50))
        
        
        
        
        self.dogsList = ["assets/images/pets/greydog.png", "assets/images/pets/yellowdog.png", "assets/images/pets/browndog.png"]
        self.dogRect = pygame.Rect(self.WIDTH/2 -70, self.HEIGHT/1.5, 150,150)
        self.dog = pygame.image.load("assets/images/pets/greydog.png")
        self.dog = pygame.transform.scale(self.dog, (150,150))
        self.arrowPressCount =0
        
    def parseDogListRight(self):
        
            
            if self.arrowPressCount < 2:
                self.arrowPressCount +=1
                self.dog = self.dogsList[self.arrowPressCount]
                return

    def parseDogListLeft(self):
        
            
            if  self.arrowPressCount >0:
                self.arrowPressCount -=1
                self.dog = self.dogsList[self.arrowPressCount]
                return
        

    def run(self):
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rightarrowRect.collidepoint(event.pos):
                       self.dog = self.parseDogListRight()
                       self.dog = pygame.image.load(self.dogsList[self.arrowPressCount])
                       self.dog = pygame.transform.scale(self.dog, (150,150))
                    elif self.leftarrowRect.collidepoint(event.pos):
                       self.dog = self.parseDogListLeft()
                       self.dog = pygame.image.load(self.dogsList[self.arrowPressCount])
                       self.dog = pygame.transform.scale(self.dog, (150,150))
                     

            # Fill the screen with white (or any color you like)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.rightArrowsurface, self.rightarrowRect.topleft)
            self.screen.blit(self.rightarrow, self.rightarrowRect.topleft) 

            pygame.draw.rect(self.screen, self.WHITE, self.leftarrowRect)
            self.screen.blit(self.leftarrow, self.leftarrowRect.topleft)
            
            
            self.screen.blit(self.dog, self.dogRect.topleft) # RGB color

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