import pygame
import random
# import winsound
from pygame import mixer

# # init = initializes
# # it will initialize all the pygame methods in program
pygame.init()
display_width = 800
display_height = 600

# args should be tuples / list... 
gameScreen = pygame.display.set_mode((display_width, display_height))
# title of the window
pygame.display.set_caption("Snake Game")

gameClose = False  

white = (255, 255, 255)
paleYellow = (255, 255, 220)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
purple = (128, 0, 128)

lead_x = display_width/2
lead_y = display_height/2

size_of_block = 10

lead_x_change = 0
lead_y_change = 0

# image of snake
img = pygame.image.load("E:/Python Pygame/Snake Game/snakeHead.png")
# image of apple
# appleimg = pygame.image.load("E:/Python Pygame/pygame/snakeHead.png")

# icon of the window...
pygame.display.set_icon(img)

# setting frame per second
clock = pygame.time.Clock()


#----------------------------Text Messages-------------------------------------
font = pygame.font.SysFont(None, 35)
smallfont = pygame.font.SysFont("Consolas", 25)
medfont = pygame.font.SysFont("Consolas", 30)
largefont = pygame.font.SysFont("Consolas", 80)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()
    # here textSurface.get_rect() returns the position of the text... 

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)

    # textRect is the positon of the text 
    textRect.center = (display_width/2), (display_height/2) + y_displace

    # it is used to display the content on the screen 
    gameScreen.blit(textSurf, textRect)


#-------------------------------  Start Menu-------------------------------
def game_intro():
    # intro = True
    while True:      # we have to loose loop here otherwise screen will stand long...
        gameScreen.fill(white)
        message_to_screen("Welcome", purple, -130, size="large")
        message_to_screen("Hope you like it", black, -60)
        message_to_screen("You should eat apples to earn points", black, -20)
        message_to_screen("If you run into yourself or run into edges, you die", black, 20)
        message_to_screen("Press Enter to play game and Q to quit", black, 180)

        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # intro = False
                    # winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
                    mixer.init()
                    mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                    mixer.music.set_volume(0.4)
                    mixer.music.play()
                    gameloop()
                if event.key == pygame.K_q:
                    quit()
#---------------------------------- Score --------------------------------------

def score(score):
    text = smallfont.render("Score : " + str(score), True, black)
    gameScreen.blit(text, [10,10])

# ------------------------------- About Snake -----------------------------------
direction = "right"
# snakelist is a list contaning another list having X & Y coordinates in it
# [ [x, y] , [x, y] , [x, y] ]...
def snake(snakelist):
    # by default img is at upward dir, So angle starts at up dir... 
    if direction == "right":
        head = pygame.transform.rotate(img, 270) # 270 deg from up dir in anti-clock wise
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    # adding image at the snake head...
    gameScreen.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    # for adding img we traverse the whole loop except snakehead... 
    # for XY in snakelist: 
    for XY in snakelist[:-1]: 
        pygame.draw.rect(gameScreen, green, [XY[0], XY[1], 20, 20])


#-------------------------------------- Main Loop-------------------------------------
def gameloop():
    global direction
    gameClose = True
    gameOver = False

    size_of_block = 10

    snakelist = []
    snakeLength = 1

    # round function convert any number into multiple of 10...
    # round(7/10.0)*10.0 = 10.0  
    # round(17/10.0)*10.0 = 20.0
    # if we do not subtract then the block will start at 800 and end at 820...
    randAppleX = round(random.randrange(0, display_width - 20)/20.0)*20.0 
    randAppleY = round(random.randrange(0, display_height - 20)/20.0)*20.0
    # for adding another apple on the screen...
    randAppleX2 = round(random.randrange(0, display_width - 20)/20.0)*20.0 
    randAppleY2 = round(random.randrange(0, display_height - 20)/20.0)*20.0 

    lead_x = display_width/2
    lead_y = display_height/2

    # by giving one var an unequal value, the snake will not remain constant,
    # it will move in one particular direction.....  
    lead_x_change = 10
    lead_y_change = 0

    while gameClose:   
        #-----------------------GAME OVER SCREEN---------------------------------
        while gameOver == True:
            gameScreen.fill(white)
            # when ever the game is over the direction is set to right......
            direction = "right"
            message_to_screen("Game Over", red, -60, size = "large")
            message_to_screen("Press Enter to play again or Q to quit", black, size = "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameClose = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameClose = False
                        gameOver = False
                    if event.key == pygame.K_RETURN:
                        # winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
                        mixer.init()
                        mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                        mixer.music.set_volume(0.4)
                        mixer.music.play()                        
                        gameloop()

        #---------------------------PLAY SCREEN------------------------------------
        # event will give whatever activites happening on the Game Screen
        # like mouseEvent, keys, button, etc.                
        for event in pygame.event.get():
            # this loop will run whenever we press the button...
            # through buttons Event will encounter and for loop runs for all the event present...
            if event.type == pygame.QUIT:
                gameClose = False

            # if user press-down keys...
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -size_of_block
                    lead_y_change = 0
                    mixer.init()
                    mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                    mixer.music.set_volume(0.4)
                    mixer.music.play()

                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = size_of_block
                    lead_y_change = 0
                    mixer.init()
                    mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                    mixer.music.set_volume(0.4)
                    mixer.music.play()

                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_x_change = 0
                    lead_y_change = -size_of_block
                    mixer.init()
                    mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                    mixer.music.set_volume(0.4)
                    mixer.music.play()

                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_x_change = 0
                    lead_y_change = size_of_block
                    mixer.init()
                    mixer.music.load("E:/Python Pygame/Snake Game/resources/move.mp3")
                    mixer.music.set_volume(0.4)
                    mixer.music.play()
                # elif event.t == pygame.KEYUP:
                #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #         lead_x_change = 0


        if lead_x >= 790 or lead_x < 0 or lead_y >= 590 or lead_y < 0:
            gameOver = True
            mixer.init()
            mixer.music.load("E:/Python Pygame/Snake Game/resources/gameover.mp3")
            mixer.music.set_volume(0.9)
            mixer.music.play()

        # on every iteration of loop, the value is added into lead_x & y for snake movement...
        lead_x += lead_x_change
        lead_y += lead_y_change

        gameScreen.fill(paleYellow)
        
        # # code for bigger apple...
        # -------------------------------------------------
        # AppleThickness = 40
        # pygame.draw.rect(gameScreen, red, (randAppleX, randAppleY, AppleThickness, AppleThickness))
        # -------------------------------------------------

        # image as an apple.....
        # gameScreen.blit(appleimg, (randAppleX, randAppleY, 20, 20))
        # # apple rect...
        pygame.draw.rect(gameScreen, red, (randAppleX, randAppleY, 20, 20))
        # for adding another apple on the screen...
        pygame.draw.rect(gameScreen, red, (randAppleX2, randAppleY2, 20, 20))

        # SNAKE------------------
        # it takes ---> ( surface , color , xcoord , ycoord , width , height )
        pygame.draw.rect(gameScreen, green, (lead_x, lead_y, 20, 20))
        # alter:
        # gameScreen.fill(red, rect = (200, 200, 50, 50))

        # on every iteration the snakelist is getting bigger through passing lead_x & y
        # if apples is not eaten by snake then the 0th element will be deleted...
        # if apple is eated by snake then the One rect will be added in snake
        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        if len(snakelist) > snakeLength :
            del snakelist[0]

        # iterates except last element 

        # Last Element in the lisy is the ----> SNAKE HEAD
        for eachSegment in snakelist[:-1]:
            if eachSegment == snakehead:
                gameOver = True
                mixer.init()
                mixer.music.load("E:/Python Pygame/Snake Game/resources/gameover.mp3")
                mixer.music.set_volume(0.9)
                mixer.music.play()

        snake(snakelist)

        score(snakeLength - 1)

        # We have to update eveything that we have changed...
        pygame.display.update()


        # old code -- when apple size is similar to snake
    # ------------------------------------------------
        if lead_x == randAppleX and lead_y == randAppleY:
            # print("yeah we got it...")
            randAppleX = round(random.randrange(0, display_width - size_of_block)/20.0)*20.0 
            randAppleY = round(random.randrange(0, display_height - size_of_block)/20.0)*20.0 
            snakeLength += 1
            # winsound.PlaySound("food.mp3", winsound.SND_ASYNC)
            # Starting the mixer
            mixer.init()
            mixer.music.load("E:/Python Pygame/Snake Game/resources/food.mp3")
            mixer.music.set_volume(0.7)
            mixer.music.play()
        
        # for adding another apple on the screen...
        if lead_x == randAppleX2 and lead_y == randAppleY2:
            # print("yeah we got it...")
            randAppleX2 = round(random.randrange(0, display_width - size_of_block)/20.0)*20.0 
            randAppleY2 = round(random.randrange(0, display_height - size_of_block)/20.0)*20.0 
            snakeLength += 1
            # winsound.PlaySound("food.mp3", winsound.SND_ASYNC)
            # Starting the mixer
            mixer.init()
            mixer.music.load("E:/Python Pygame/Snake Game/resources/food.mp3")
            mixer.music.set_volume(0.7)
            mixer.music.play()
            
    # ------------------------------------------------
        # new code -- when apple is slightly bigger
        # if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness:
        #     if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
        #         randAppleX = round(random.randrange(0, display_width - size_of_block)/20.0)*20.0 
        #         randAppleY = round(random.randrange(0, display_height - size_of_block)/20.0)*20.0 
        #         snakeLength += 1

        # 15 = frame per second
        clock.tick(30)
    quit()

game_intro() # fu5n call
