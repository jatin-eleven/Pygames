import turtle
import winsound


wn = turtle.Screen()
wn.title("Pong Game @JatinEleven")
wn.bgcolor("black")
wn.setup(width=800, height=600)
# stops the window from updating... which helps to speed up the games quite.
wn.tracer(0)


#score
score_a = 0
score_b = 0


# Paddle A...
    # module name . class name 
paddle_a =  turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")

# by default size is 20px by 20px...
# stretch width by 5 times of default and length by 1... 
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
# position...
paddle_a.goto(-360, 0)




# Paddle B...
    # module name . class name 
paddle_b =  turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")

# by default size is 20px by 20px...
# stretch width by 5 times of default and length by 1... 
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
# position...
paddle_b.goto(360, 0)



# Ball...
ball =  turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)

# everytime ball moves by 0.3 speed in x and y dir simaltaneously...which is diagnol dir
ball.dx = 0.4   # d = delta or change
ball.dy = -0.4   
# here speed is dependent on the computer... (2 is normal on mosty of the computer)
# here it is very fast on 2


#pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A : 0   Player B : 0", align="center", font=("Courier", 24, "bold"))




# Function 
def paddle_a_up():
    # gives the coordinate
    y = paddle_a.ycor()
    # increase the coordinate by 20
    y += 40
    paddle_a.sety(y)


def paddle_a_down():
    # gives the coordinate
    y = paddle_a.ycor()
    # increase the coordinate by 20
    y -= 40
    paddle_a.sety(y)


def paddle_b_up():
    # gives the coordinate
    y = paddle_b.ycor()
    # increase the coordinate by 20
    y += 40
    paddle_b.sety(y)


def paddle_b_down():
    # gives the coordinate
    y = paddle_b.ycor()
    # increase the coordinate by 20
    y -= 40
    paddle_b.sety(y)



# Keyboard binding
# it starts listinig the keyboard...
wn.listen()
# when we press "w" paddle_a_up fun is called...
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")

wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")



# main...
while True:
    wn.update()

    # move ball 
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)


    # border checking
    if paddle_a.ycor() > 260:
        paddle_a.sety(260)
    
    if paddle_a.ycor() < -260:
        paddle_a.sety(-260)

    if paddle_b.ycor() > 260:
        paddle_b.sety(260)

    if paddle_b.ycor() < -260:
        paddle_b.sety(-260)



    if ball.ycor() > 280:
        # if it is greater than 290 set it back to 290 again...
        ball.sety(280)
        # it reverse the direction 
        # which creates a striking effect...
        ball.dy *= -1
        # plays the sound
        # syntax for Windows - it depends upon the OS 
        winsound.PlaySound("E:/Python Pygame/Pong Game/bounce.wav", winsound.SND_ASYNC)


    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1
        # plays the sound
        # syntax for Windows - it depends upon the OS 
        winsound.PlaySound("E:/Python Pygame/Pong Game/bounce.wav", winsound.SND_ASYNC)

    
    if ball.xcor() > 390:
        # goes to center 
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1  
        ball.color("red") 
        pen.clear()    
        pen.write("Player A :{}   Player B : {}".format(score_a, score_b), align="center", font=("Courier", 24, "bold"))


    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1        
        ball.color("red") 

        pen.clear()  
        pen.write("Player A :{}   Player B : {}".format(score_a, score_b), align="center", font=("Courier", 24, "bold"))



    # paddle and ball collision
    if(ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 60 and ball.ycor() > paddle_b.ycor() - 60):
        ball.setx(340)
        ball.dx *= -1
        ball.color("white") 

        # plays the sound
        # syntax for Windows - it depends upon the OS 
        winsound.PlaySound("E:/Python Pygame/Pong Game/bounce.wav", winsound.SND_ASYNC)

    if(ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 60 and ball.ycor() > paddle_a.ycor() - 60):
        ball.setx(-340)
        ball.dx *= -1 
        ball.color("white") 
            
        # plays the sound
        # syntax for Windows - it depends upon the OS 
        winsound.PlaySound("E:/Python Pygame/Pong Game/bounce.wav", winsound.SND_ASYNC)