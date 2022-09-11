# it allows us to use all pygame commands without using pygame keyword...
import pygame
from pygame.locals import * 
from OpenGL.GL import *
from OpenGL.GLU import *


# it should be in tuples 
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),    
    (0, 3),
    (0, 4),    
    (2, 1),
    (2, 3), 
    (2, 7),    
    (6, 3), 
    (6, 4), 
    (6, 7), 
    (5, 1), 
    (5, 4), 
    (5, 7)    
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)


def Draw():
    glBegin(GL_LINES)
    for edge in edges:
        for node in edge:
            glColor3fv((1, 0, 0))
            glVertex3fv(vertices[node])
    glEnd()

    glBegin(GL_QUADS)
    for surface in surfaces:
        for node in surface:
            glColor3fv((0, 1, 0))
            glVertex3fv(vertices[node])
    glEnd()



def main():
    pygame.init()
    display = (800, 600)
    # display loads in buffer and openGl is just a parameter 
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #used to cliping the some part of the object...
    gluPerspective(45.0, (display[0] / display[1]), 1 , 50.0)

    # moving backward direction...
    glTranslatef(0.0, 0.0, -5.0)

    # current position of cube...
    glRotatef(40, 20, 20, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 0.0, 1.0)
                if event.button == 5:
                    glTranslatef(0.0, 0.0, -1.0)

    
        glRotatef(1, 1, 1, 1)

        # basically it clears the pygame background....
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Draw()

        pygame.display.flip() # used to update..... 
        # just like pygame.display.update()
        
        pygame.time.wait(10)

# fun call
main()
