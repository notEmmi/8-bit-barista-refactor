import pygame
import config
import math
import samplestartscreen
import start_menu

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")

clock = pygame.time.Clock()

TIMER_EVENT_STAR = pygame.USEREVENT + 1  
TIMER_EVENT_CLOUD = pygame.USEREVENT + 2  
TIMER_EVENT_FADEOUT = pygame.USEREVENT + 3

pygame.time.set_timer(TIMER_EVENT_STAR, 150)
pygame.time.set_timer(TIMER_EVENT_CLOUD, 100)
pygame.time.set_timer(TIMER_EVENT_FADEOUT, 5000)

CLOUDX = 25 
CLOUDY=150


def updateCloud(dx, dy):

    global CLOUDX
    global CLOUDY

    if(CLOUDX >=700):
        CLOUDX = 25



    CLOUDX += dx
    CLOUDY +=dy

    # print("cloud x pos = ", CLOUDX, "\n", "cloud y pos =", CLOUDY)
 

    return CLOUDX, CLOUDY


## load images ########

tree = pygame.image.load("images/tree.png")
tree = pygame.transform.scale(tree, config.TREE_SIZE )


grass = pygame.image.load("images/grass.png")
grass = pygame.transform.scale(grass, config.GRASS_SIZE )

star = pygame.image.load("images/star.png")
star = pygame.transform.scale(star, config.STARSIZE )

loading = pygame.image.load("images/loading.png")
loading = pygame.transform.scale(loading, config.LOADING_SIZE )

cloud = pygame.image.load("images/cloud.png")
cloud = pygame.transform.scale(cloud, config.CLOUD_SIZE )


# Set up colors
WHITE = (255, 255, 255)

# Game loop
running = True
while running:
    screen.fill(config.LIGHT_PURPLE)  # Fill screen with white
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
    
    
        if event.type == TIMER_EVENT_STAR:
             config.updateStar(config.STARDX,config.STARDY)

        time = pygame.time.get_ticks()

        CLOUD_DX = 10
        CLOUD_DY = math.trunc(math.sin(time) *10)
            

        if event.type == TIMER_EVENT_CLOUD:
            
             updateCloud(CLOUD_DX, CLOUD_DY)


        if event.type == TIMER_EVENT_FADEOUT:
             ## ADD LOGIC TO MOVE TO APPROPRATE SCREEN WHEN POSSILBE ####
             start_menu.runStartMenu()
             running = False
    
    screen.blit(star, (config.STARX, config.STARY))
    screen.blit(cloud, (CLOUDX, CLOUDY))

    screen.blit(grass, (config.GRASS_LOC))
    screen.blit(tree, config.TREE_LOC)
    screen.blit(loading, config.LOADING_LOC)
    

    
    

    
    pygame.display.flip()  # Update display
    clock.tick(30)
# Quit Pygame
pygame.quit()




