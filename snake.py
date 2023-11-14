#Import libraries
import pygame
import argparse

pygame.init()


#Initialize constants
WHITE = (255,255,255) 
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WIDTH = 400
HEIGTH = 300
SIZE_OF_SQUARE = 20
CLOCK_FREQUENCY = 2
RIGHT = (1,0)
LEFT = (-1,0)
TOP = (0,-1)
DOWN = (0,1)
POS_FRUIT_1 = (3,3)
POS_FRUIT_2 = (15,10)

#Command line arguments 

    #Create arguments
parser = argparse.ArgumentParser(description = 'Some description')
parser.add_argument('--bg-color-1', help ='first color of the background', default = WHITE)
parser.add_argument('--bg-color-2',help='second color of the background', default = BLACK)
parser.add_argument('--height', type = int, help='window height', default = HEIGTH)
parser.add_argument('--width', type = int,help='window width', default = WIDTH)
parser.add_argument('--fps', type = int,help='the number of frames per second', default = CLOCK_FREQUENCY)
parser.add_argument('--fruit-color', help = 'color of the fruit', default = RED)
parser.add_argument('--snake-color', help="snake color", default = GREEN)
parser.add_argument('--snake-length', type = int,help='initial length of the snake', default = 3)
parser.add_argument('--tile-size', type = int, help='size of a square tile', default = SIZE_OF_SQUARE)
args = parser.parse_args()

    #Raise errors if it's not the right value
if (args.height)%(args.tile_size)!= 0 :
    raise ValueError ("The height (-height argument) must be a multiple of (-tile_size)")
if (args.width)%(args.tile_size)!= 0 :
    raise ValueError ("The width (-width argument ) must be a multiple of (-tile_size)")
if (args.width)//(args.tile_size)< 20 :
    raise ValueError ("There must be at least 20 columns")
if (args.height)//(args.tile_size)< 12 :
    raise ValueError ("There must be at least 12 rows")
if (args.snake_length)< 2 :
    raise ValueError ("The snake (-snake_length argument) should not be lower than 2")
if (args.snake_length)> 13 :
    raise ValueError ("The snake (-snake_length argument) should not be lower than 2")
if (args.bg_color_1)==(args.snake_color) or (args.bg_color_1)==(args.bg_color_2) or (args.bg_color_2)==(args.snake_color):
    raise ValueError ("The color of the snake ans the colors of the checkboard should not be identical")

#Initialize global variables
    #Creation of snake
snake=[]
for i in range(args.snake_length):
    snake.append((10,5+i))

direction = TOP
fruit = (3,3)
score = 0

#Create a screen
screen = pygame.display.set_mode( (args.width, args.height ))

#Create a clock
clock = pygame.time.Clock()

#Loop forever
execute = True      
while execute :
    clock.tick(args.fps)

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
    n=args.width//args.tile_size
    m=args.height//args.tile_size  
        #Background
    screen.fill(args.bg_color_2) 
        #Black squares
    for i in range(n):
        for j in range(m):
            if (i+j)%2==0:
                rectangle=pygame.Rect(i*args.tile_size,j*args.tile_size,args.tile_size,args.tile_size)
                pygame.draw.rect(screen,args.bg_color_1,rectangle)

    #New head
    new_head_pos = (snake[0][0]+direction[0],snake[0][1]+direction[1])
    snake.insert(0,new_head_pos)

    #Fruit has not been eaten
    if new_head_pos != fruit :
         #Delete queue
        snake.pop()

    #Fruit has been eaten
    else :
        #Switch fruit position
        if fruit == POS_FRUIT_1 :
            fruit = POS_FRUIT_2
        else :
            fruit = POS_FRUIT_1
        #Update score
        score = score + 1

    #Draw fruit 
    rectangle_red = pygame.Rect(fruit[0]*args.tile_size,fruit[1]*args.tile_size,args.tile_size,args.tile_size)
    pygame.draw.rect(screen,args.fruit_color,rectangle_red)

    #Draw snake
    for (x,y) in snake :
        rectangle_green= pygame.Rect(x*args.tile_size,y*args.tile_size,args.tile_size,args.tile_size)
        pygame.draw.rect(screen,args.snake_color,rectangle_green)

    #Display the screen
    pygame.display.update()
    pygame.display.set_caption(f"Score : {score}")

#Turn off pygame
pygame.quit()

#Quit properly
quit(0)  

