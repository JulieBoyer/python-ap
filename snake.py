import pygame

pygame.init()

#Initialize constants
WHITE = (255,255,255) 
BLACK = (0,0,0)
GREEN = (0,255,0)
WIDTH = 400
HEIGTH = 300
SIZE_OF_SQUARE = 20
CLOCK_FREQUENCY = 1
RIGHT = (1,0)
LEFT = (-1,0)
TOP = (0,-1)
DOWN = (0,1)

#Initialize global variables
snake = [(10,5),(10,6),(10,7)]
#       head            queue
direction = TOP

#Create a screen
screen = pygame.display.set_mode( (WIDTH, HEIGTH) )

#Create a clock
clock = pygame.time.Clock()

#Loop forever
execute = True      
while execute :
    clock.tick(CLOCK_FREQUENCY)
   #Process new events
    for event in pygame.event.get():
        #Catch a key press
        if event.type == pygame.KEYDOWN :  
            #Q has been press 
            if event.key == pygame.K_q :        
                execute = False 
            #Arrow key has been presss => need to change direction
            if event.key == pygame.K_RIGHT : 
                 direction = RIGHT
            if event.key == pygame.K_LEFT : 
                 direction = LEFT
            if event.key == pygame.K_UP : 
                 direction = TOP
            if event.key == pygame.K_DOWN : 
                 direction = DOWN  
        #Catch selection of exit icon       
        if event.type == pygame.QUIT :     
                execute = False
    #Draw the checkerboard
        #Number of rows and columns
    n=WIDTH//SIZE_OF_SQUARE
    m=HEIGTH//SIZE_OF_SQUARE   
        #Background
    screen.fill(WHITE) 
        #Black squares
    for i in range(n):
        for j in range(m):
            if (i+j)%2==0:
                rectangle=pygame.Rect(i*SIZE_OF_SQUARE,j*SIZE_OF_SQUARE,SIZE_OF_SQUARE,SIZE_OF_SQUARE)
                pygame.draw.rect(screen,BLACK,rectangle)
    #New head
    snake.insert(0,(snake[0][0]+direction[0],snake[0][1]+direction[1]))
    #Delete queue
    snake.pop()
    #Draw snake
    for (x,y) in snake :
        rectangle_green= pygame.Rect(x*SIZE_OF_SQUARE,y*SIZE_OF_SQUARE,SIZE_OF_SQUARE,SIZE_OF_SQUARE)
        pygame.draw.rect(screen,GREEN,rectangle_green)
    #Display the screen
    pygame.display.update()
#Turn off pygame
pygame.quit()
#Quit properly
quit(0)  

