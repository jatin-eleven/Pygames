import pygame
import sys
import math

pygame.init()

# window setup...
SCREEN_WIDTH = 480*2
SCREEN_HEIGHT = 480
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycaster 3D")

# init clock...
clock = pygame.time.Clock()

# global constants
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH/2) / MAP_SIZE)   # 60
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)          # 480
FOV = math.pi/3                                # 1.04666...
HALF_FOV = FOV/2                               # 0.52333...
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS                 # 0.00872...
SCALE = (SCREEN_WIDTH/2) / CASTED_RAYS         # 4


MAP = (
    "########"
    "# #    #"
    "# #  ###"
    "#      #"
    "#      #"
    "#  ##  #"
    "#   #  #"
    "########"
)
# map indexes are like this...
# MAP = (
#   0,1,2,3,4,5,6,7
#   8,9,10,11,12,13,14,15
#   ...................
#   ...................
# )


# global variables
player_x = (SCREEN_WIDTH/ 2) /2                # 240
player_y = (SCREEN_WIDTH/ 2) /2                # 240
player_angle = math.pi                         # 3.14

# Function to Draw Map...
def draw_map():
    for row in range(8):          # loop over map rows
        for col in range(8):          # loop over map cols 
            # calculate square index
            square = row * MAP_SIZE + col      # (0,1,2,3,4,5,6,7,8,9,10,11,)

            # draw map in the window (drawing grey and dark grey boxes)
            pygame.draw.rect(win, 
                (200,200,200) if MAP[square] == "#"
                else (100,100,100),
                    #         postion                    dimensions
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1))


    # draw player on the map
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

    # player direction - (center line)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle) * 100,
                                        player_y + math.cos(player_angle) * 100), 3) 
    # draw player FOV - (left and right line)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle - HALF_FOV) * 100,
                                        player_y + math.cos(player_angle - HALF_FOV) * 100), 3) 
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle + HALF_FOV) * 100,
                                        player_y + math.cos(player_angle + HALF_FOV) * 100), 3) 



# raycasting algorithim 
def cast_rays():
    # define left most angle of FOV 
    start_angle = player_angle - HALF_FOV   

    # loop over casted rays 
    for ray in range(CASTED_RAYS):
        # cast rays step by step 
        for depth in range(MAX_DEPTH):
            # get ray target coordinates 
            target_x = player_x - math.sin(start_angle) * depth  
            target_y = player_y + math.cos(start_angle) * depth

            # converting target x and y coordinate to map row and Col
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # calculate map square index 
            sqaure = row * MAP_SIZE + col
            
            # if rays hits the wall
            if MAP[sqaure] == "#":
                pygame.draw.rect(win, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2))
                
                # draw casted rays 
                pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y)) 
                
                # wall shading
                color = 155 / (1 + depth * depth * 0.0001) # just to avoid by zero

                # fixing fish eye effect...
                depth *= math.cos(player_angle - start_angle)

                # calulate wall height
                wall_height = 21000/(depth + 0.0001) 
                
                # fix stuck at the wall
                # if wall_height > SCREEN_HEIGHT :
                #     wall_height = SCREEN_HEIGHT 

                # draw 3D projection (rectangle by rectangle.....)
                pygame.draw.rect(win, (color+50, color, color+70), (SCREEN_HEIGHT + ray * SCALE, (SCREEN_HEIGHT/2) - wall_height/2, SCALE, wall_height))
                 
                break
    
        # increment angle by a single step 
        start_angle += STEP_ANGLE


# moving directon 
forward = True

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # converting target x aand y coordinate to map row and Col
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    # calculate map square index 
    sqaure = row * MAP_SIZE + col

    # player hits the wall (Collision detection)
    if MAP[sqaure] == "#":
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5


    # update 2D backgroud
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))
    # update 3D backgroud
    pygame.draw.rect(win, (180, 120, 200), (480, SCREEN_HEIGHT/2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT/2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    
    # draw 2D map 
    draw_map()

    cast_rays()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5


    # set FPS
    clock.tick(30)

    # display FPS
    fps = str(int(clock.get_fps()))
    
    # pick up the font
    font = pygame.font.SysFont('Monospace Regular', 30)
    
    # create font surface
    fps_surface = font.render(fps, False, (255, 255, 255))
    
    # print FPS to screen
    win.blit(fps_surface, (480, 0))

    # update display
    pygame.display.flip()



