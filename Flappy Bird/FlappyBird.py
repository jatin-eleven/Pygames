import random
import sys        # We will use sys to exit the program...
from typing import List     
import pygame
from pygame.locals import *

#Global Variables
FPS = 32
SCREENWIDTH = 289   
SCREENHEIGHT = 511

#initialize the screen or display...
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUNDY = SCREENHEIGHT * 0.8

GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYERS = "Flappy Bird/gallery/sprites/bird.png"
BACKGROUND = "Flappy Bird/gallery/sprites/background.png"
PIPE = "Flappy Bird/gallery/sprites/pipe.png"

img = pygame.image.load("E:/Python Pygame/Flappy Bird/gallery/sprites/bird.png")
pygame.display.set_icon(img)

white = (255, 255, 255)
purple = (128, 0, 128)
text1 = "Flappy Bird"
text2 = "Let's Play"
# text3 = "Let's Play"


def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    # player is exactly at the center of the Y-axis 
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)
    
    # messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_width())/2)
    # messagey = int(SCREENHEIGHT * 0.13)
    messagex = 25
    messagey = int(SCREENHEIGHT * 0.13)

    medfont = pygame.font.SysFont("Consolas", 40, bold = True)
    smallfont = pygame.font.SysFont("Consolas", 20, bold = True)
    textSurface1 = medfont.render(text1, True, white)
    textSurface2 = smallfont.render(text2, True, white)

    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            # elif event.type == KEYDOWN and (event.key == K_RETURN):
                return  #this fun is completed...

            # elif event.type == KEYDOWN and (event.key == pygame.K_RETURN):
            else:
                SCREEN.blit(GAME_SPRITES["background"], (0,0))
                SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))

                # SCREEN.blit(GAME_SPRITES["message"], (messagex, messagey))

                SCREEN.blit(textSurface1, (messagex, messagey))
                SCREEN.blit(textSurface2, (messagex + 60, messagey + 45))

                SCREEN.blit(GAME_SPRITES["base"], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx =  int(SCREENWIDTH/5)
    playery =  int(SCREENWIDTH/2)
    basex = 0

    #create 2 pipes for blitting on the screen...
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes...
    upperPipes = [
        {"x" : SCREENWIDTH + 250, "y" : newPipe1[0]["y"]},
        {"x" : SCREENWIDTH + 250 + (SCREENWIDTH / 2) + 30, "y" : newPipe2[0]["y"]}
    ]

    #list of lower pipes...
    lowerPipes = [
        {"x" : SCREENWIDTH + 250, "y" : newPipe1[1]["y"]},
        {"x" : SCREENWIDTH + 250 + (SCREENWIDTH / 2) + 30, "y" : newPipe2[1]["y"]}
    ]
    ''' here "x" is the difference between 2 individual pipes'''


    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8     # Velocity while flapping...
    playerFlapped = False   # It is true only when bird is flapping...

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY  = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()
        
        #this fun will return true if player is crashed.....
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            return

        #check for score...
        playerMidPos = playerx + GAME_SPRITES["player"].get_width() / 2

        for pipe in upperPipes:
            pipeMidPos = pipe["x"] + GAME_SPRITES["pipe"][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"your score is : {score}")
                GAME_SOUNDS["point"].play()
        

        if playerVelY < playerMaxVelY and not playerFlapped:
        # if not playerFlapped:
            playerVelY += playerAccY 

        if playerFlapped:
            playerFlapped = False

        ''' in case of not Flapping :
        here first playery goes upward and after that it countiniously decreasing with increasing acceleration...
        '''

        ''' in case of Flapping :
        it increasing on the KeyTap by -8px and decrease by increasing amt of acceleration...        '''
        # playerHeight = GAME_SPRITES["player"].get_height()
        # playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        playery = playery + playerVelY     # -----changed-----


        #Move pipes to the left...
        '''
        a = (1, 2, 3, 4)
        b = (6, 7, 8, 9)
            zip(a, b)
        zip : basically it gives the pairs of tuple, lists....
        output will be...
        ===> (1, 6) (2, 7) (3, 8) (4, 9)
        '''
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe["x"] += pipeVelX
            lowerpipe["x"] += pipeVelX

        # add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]["x"] < 5:
            
            newpipe = getRandomPipe()

            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it...
        if upperPipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperPipes.pop(0) 
            lowerPipes.pop(0) 

        # lets blit our SPRITES now
        SCREEN.blit(GAME_SPRITES["background"], (0, 0))
        
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0], (upperpipe["x"], upperpipe["y"]))
            SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerpipe["x"], lowerpipe["y"]))

        SCREEN.blit(GAME_SPRITES["base"], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))

        myDigit = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigit:
            width += GAME_SPRITES["numbers"][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigit:
            SCREEN.blit(GAME_SPRITES["numbers"][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES["numbers"][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS["hit"].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES["pipe"][0].get_height()
        
        if (playery < pipeHeight + pipe["y"] and abs(playerx - pipe["x"]) + 20 < GAME_SPRITES["pipe"][0].get_width()):
            GAME_SOUNDS["hit"].play()
            return True
        
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) + 20 < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
            
    return False


# Generate positions of the pipes...
def getRandomPipe():
    pipeHeight = GAME_SPRITES["pipe"][0].get_height()
    # offset = SCREENHEIGHT/3 #=== approx 160
    offset = random.randrange(110, int(SCREENHEIGHT/3))
    
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES["base"].get_height() - 1.2 * offset))
    '''  y2 = 160 (offset height) + random in between (0 to 320) (actual pipe)  '''

    '''
    basically pipeX is the difference between set of 2 pipes....
    like this :  | |    | |    | |    | |    '''
    pipeX = SCREENWIDTH + 70

    y1 = pipeHeight - y2 + offset

    pipe = [
        {"x" : pipeX, "y" : -y1},   # upper pipe
        {"x" : pipeX, "y" : y2}     # lower pipe
    ]
    return pipe



# This will be the main point where the game will start...
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    
    GAME_SPRITES["numbers"] = (
        # convert_alpha ===> used to optimise the image for games
        pygame.image.load("Flappy Bird/gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("Flappy Bird/gallery/sprites/9.png").convert_alpha(),
    )

    # GAME_SPRITES["message"] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    
    GAME_SPRITES["base"] = pygame.image.load("Flappy Bird/gallery/sprites/base.png").convert_alpha()
    
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #Game Sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound("Flappy Bird/gallery/audio/die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("Flappy Bird/gallery/audio/hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("Flappy Bird/gallery/audio/point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("Flappy Bird/gallery/audio/swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("Flappy Bird/gallery/audio/wing.wav")

    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["player"] = pygame.image.load(PLAYERS).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()


