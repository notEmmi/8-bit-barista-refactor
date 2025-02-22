### colors ####
WHITE = (255, 255, 255)
LIGHT_PURPLE = (200, 162, 200)
DARK_PURPLE = (150, 112, 150)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

## asset locations load screen ######
GRASS_LOC = -35,450
LOADING_LOC = 225, 50
TREE_LOC = 50, 250


TREE_SIZE = 250, 350
GRASS_SIZE = 900, 150
LOADING_SIZE = 350, 125

### vars needed for moving star

X ,Y = 100, 300
DX, DY = 100, -50
STARSIZE = (50,50)





### animation fucntions ####





def updateStar(dx,dy):
    
    global X, Y  # Access and modify global variables

    if(X >=600):
        X = 100
        Y= 300
    X += dx
    Y += dy
    return X, Y  # Return updated values

    






 




