#Import libraries
import pygame
import argparse
import logging
import operator
import sys 
import os

#Initialize the Pygame libraty
pygame.init()

#Initialize constants
WHITE = (255,255,255) 
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WIDTH = 400
HEIGTH = 300
SIZE_OF_SQUARE = 20
CLOCK_FREQUENCY = 5
RIGHT = (1,0)
LEFT = (-1,0)
TOP = (0,-1)
DOWN = (0,1)
POS_FRUIT_1 = (3,3)
POS_FRUIT_2 = (15,10)
MIN_WND_SIZE = 200
MIN_SNAKE_LEN = 2 
MAX_SNAKE_LEN = 12
MIN_TILE_SIZE = 10 
MIN_NB_ROWS = 12
MIN_NB_COLS = 20

#Definition of useful functions

    #Function for command line arguments 
def read_args():
    #Create arguments
    parser = argparse.ArgumentParser(description = 'Implementation of the snake game')
    parser.add_argument('--bg-color-1', help ='first color of the background', default = WHITE)
    parser.add_argument('--bg-color-2',help='second color of the background', default = BLACK)
    parser.add_argument('--height', type = int, help='window height', default = HEIGTH)
    parser.add_argument('--width', type = int,help='window width', default = WIDTH)
    parser.add_argument('--fps', type = int,help='the number of frames per second', default = CLOCK_FREQUENCY)
    parser.add_argument('--fruit-color', help = 'color of the fruit', default = RED)
    parser.add_argument('--snake-color', help="snake color", default = GREEN)
    parser.add_argument('--snake-length', type = int,help='initial length of the snake', default = 3)
    parser.add_argument('--tile-size', type = int, help='size of a square tile', default = SIZE_OF_SQUARE)
    parser.add_argument('--gameover-on-exit', help = 'A flag', action = 'store_true')
    parser.add_argument('--debug','-g', help='Set debug mode.',action='store_true')
    parser.add_argument('--high-scores-file', default =os.path.join(os.environ['HOME'],'.snake_scores.txt'),help="The path to the file in which to store high score.")
    parser.add_argument('--max-high-scores',type = int, default=5,help="The maximum of high score to store")
    args = parser.parse_args()
    #Raise errors if it's not the right value
    if args.height < MIN_WND_SIZE or args.width < MIN_WND_SIZE:
        raise ValueError ("Window height and width must be greater or equal to %d.")
    if (args.height)%(args.tile_size)!= 0 :
        raise ValueError ("The height (-height argument) must be a multiple of (-tile_size)")
    if (args.width)%(args.tile_size)!= 0 :
        raise ValueError ("The width (-width argument ) must be a multiple of (-tile_size)")
    if (args.width)//(args.tile_size)< MIN_NB_COLS :
        raise ValueError ("There must be at least 20 columns")
    if (args.height)//(args.tile_size)< MIN_NB_ROWS :
        raise ValueError ("There must be at least 12 rows")
    if (args.snake_length)< MIN_SNAKE_LEN :
        raise ValueError ("The snake (-snake_length argument) should not be lower than 2")
    if (args.snake_length)> MAX_SNAKE_LEN :
        raise ValueError ("The snake (-snake_length argument) should not be lower than 2")
    if (args.bg_color_1)==(args.snake_color) or (args.bg_color_1)==(args.bg_color_2) or (args.bg_color_2)==(args.snake_color):
        raise ValueError ("The color of the snake and the colors of the checkboard should not be identical")
    return(args)

def update_high_scores(scores,new_score,max_scores):
    #Add new score
    if new_score > 0 and (len(scores) < max_scores or new_score > scores[0][0]):
        name = input("Write your name :")
        scores.append((new_score,name))
        shorten_high_scores(scores,max_scores)

def print_high_scores(scores,logger):
    if len(scores)>0:
        logger.info("\nHIGH SCORES :")
        for (b,a) in scores[::-1]:
            print(a+': '+str(b))

#Function to read scores and return the list scores
def read_scores(path_of_file):
    scores = []
    if os.path.exists(path_of_file): 
        with open(path_of_file,'r') as f:
            for line in f :
                line=line.strip()
                line=line.split()
                a,b=line
                b=int(b)
                scores.append((b,a))
    scores.sort(key=lambda x : x[0])
    return scores 

#Function to update the file for high scores
def write_scores(scores,name_path):
    if scores != read_scores(name_path) : 
        with open (name_path, 'w') as f :
            for (b,a) in scores :
                print(a+' '+str(b), file = f)


def shorten_high_scores(scores,max_scores):
    if len(scores)>max_scores:
        scores.pop(0)


    #Function to process events
def process_events(execute,event,direction):
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
    return(execute,direction)

    #Function to get score
def get_score (snake,args):
    score = len(snake)-args.snake_length
    return(score)

    #Function to draw the checkerboard
def draw_checkerboard(screen,args):
    #Number of rows and columns
    n=args.width//args.tile_size
    m=args.height//args.tile_size  
    #Background
    screen.fill(args.bg_color_1) 
    #Black squares
    for i in range(n):
        for j in range(m):
            if (i+j)%2==0:
                rectangle=pygame.Rect(i*args.tile_size,j*args.tile_size,args.tile_size,args.tile_size)
                pygame.draw.rect(screen,args.bg_color_2,rectangle)
    return(n,m)

    #Function to draw fruit 
def draw_fruit(fruit,screen,args):
    rectangle_red = pygame.Rect(fruit[0]*args.tile_size,fruit[1]*args.tile_size,args.tile_size,args.tile_size)
    pygame.draw.rect(screen,args.fruit_color,rectangle_red)

    #Function to draw snake
def draw_snake(snake,screen,args):
    for (x,y) in snake:
        rectangle_green= pygame.Rect(x*args.tile_size,y*args.tile_size,args.tile_size,args.tile_size)
        pygame.draw.rect(screen,args.snake_color,rectangle_green)

    #Function to draw everything
def draw(snake,fruit,screen,args):
    n,m = draw_checkerboard(screen,args)
    draw_fruit(fruit,screen,args)
    draw_snake(snake,screen,args)
    return(n,m)

    #Function to update display
def update_display(snake,args,fruit,screen):
    draw(snake,fruit,screen,args)
    #Display the screen
    pygame.display.update()
    #To add the score in the caption
    pygame.display.set_caption("Snake - score: %d"
            % (get_score(snake,args)))

    #Function to make the snake
def move_snake(new_head_pos,snake,fruit):
    snake.insert(0,new_head_pos)
    #Fruit has not been eaten
    if new_head_pos != fruit :
         #Delete queue
        snake.pop()
    return (snake)

    #Function to change the position of the fruit if it has been eaten
def update_fruit(new_head_pos,fruit,logger):  
    #Fruit has been eaten
    if new_head_pos == fruit :
        #Print an debug message 
        logger.debug("Snake has eaten a fruit.")
        #Switch fruit position
        if fruit == POS_FRUIT_1 :
            fruit = POS_FRUIT_2
        else :
            fruit = POS_FRUIT_1
    return(fruit,logger)

    #Function to handle exit
def handle_exit(new_head_pos,n,m,snake,execute,args) :
    #Handle snake exit
    if new_head_pos[0] ==-1 : 
        if args.gameover_on_exit :
            execute = False
        else :
            snake[0]=(n-1,new_head_pos[1])
    if new_head_pos[0] == n:
        if args.gameover_on_exit :
            execute = False
        else :
            snake[0]=(0,new_head_pos[1])
    if new_head_pos[1]==-1 :
        if args.gameover_on_exit :
            execute = False
        else :
            snake[0]=(new_head_pos[0],m-1)
    if new_head_pos[1]==m:
        if args.gameover_on_exit :
            execute = False
        else :
            snake[0]=(new_head_pos[0],0)
    return (snake,execute)

    #Function to handle collision
def handle_collision(snake,execute):
    for position, (a,b) in enumerate(snake):
        if snake[0]==(a,b) and position != 0 :
            execute = False 
    return (execute)

#Main function
def main():
    #Read arguments
    args = read_args()

    #Setup the logger
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    #Initialize of old global variables and now local variables for the function main
        #Creation of snake
    snake=[]
    for i in range(args.snake_length):
        snake.append((10,5+i))
        #Initialize direction
    direction = TOP
        #Initialize fruit position
    fruit = POS_FRUIT_1
        #Create a screen
    screen = pygame.display.set_mode( (args.width, args.height ))
        #Create a clock
    clock = pygame.time.Clock()

    #Loop forever
    execute = True 
        #Print an debug message
    logger.debug("Start main loop.") 
    while execute :
        clock.tick(args.fps)
        #Process new events
        for event in pygame.event.get():
            execute,direction = process_events(execute,event,direction)
        #Consider the new position of the head
        new_head_pos = (snake[0][0]+direction[0],snake[0][1]+direction[1])
        #Move snake
        snake = move_snake(new_head_pos,snake,fruit)
        #Move fruit and print message if the fruit has been eaten
        fruit,logger = update_fruit(new_head_pos,fruit,logger)
        #Draw
        n,m = draw(snake,fruit,screen,args)
        #Handle exit
        snake,execute = handle_exit(new_head_pos,n,m, snake,execute,args)
        #Handle collision
        execute = handle_collision(snake,execute)
        #Update display
        update_display(snake,args,fruit,screen)

    #Message when the game is over
    logger.info("GAME OVER !")

    #High scores
    scores = read_scores(args.high_scores_file)
    update_high_scores(scores,get_score(snake,args),args.max_high_scores)
    write_scores(scores,args.high_scores_file)
    print_high_scores(scores,logger)
#Call the function main
main()

#Turn off pygame
pygame.quit()

#Quit properly
quit(0)  