import pygame
import config


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")

clock = pygame.time.Clock()

TIMER_EVENT = pygame.USEREVENT + 1  
pygame.time.set_timer(TIMER_EVENT, 300)



## load images ########

tree = pygame.image.load("images/tree.png")
tree = pygame.transform.scale(tree, config.TREE_SIZE )


grass = pygame.image.load("images/grass.png")
grass = pygame.transform.scale(grass, config.GRASS_SIZE )

star = pygame.image.load("images/star.png")
star = pygame.transform.scale(star, config.STARSIZE )

loading = pygame.image.load("images/loading.png")
loading = pygame.transform.scale(loading, config.LOADING_SIZE )

# Set up colors
WHITE = (255, 255, 255)

# Game loop
running = True
while running:
    screen.fill(config.LIGHT_PURPLE)  # Fill screen with white
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
        if event.type == TIMER_EVENT:
             config.updateStar(config.DX,config.DY)
    
    
    
    screen.blit(star, (config.X, config.Y))
    screen.blit(grass, (config.GRASS_LOC))
    screen.blit(tree, config.TREE_LOC)
    screen.blit(loading, config.LOADING_LOC)
    
    

    
    pygame.display.flip()  # Update display
    clock.tick(30)
# Quit Pygame
pygame.quit()
