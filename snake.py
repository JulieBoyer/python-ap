import pygame

pygame.init()

#Initialize constants

WHITE = (255,255,255) 

BLACK = (0,0,0)

GREEN = (0,255,0)

WIDTH = 400

HEIGTH = 300

screen = pygame.display.set_mode( (WIDTH, HEIGTH) )

clock = pygame.time.Clock()

SIZE_OF_SQUARE = 20

CLOCK_FREQUENCY = 7

RIGHT = (1,0)

LEFT = (-1,0)

TOP = (0,-1)

DOWN = (0,1)

snake = [(10,5),(10,6),(10,7)]

execute = True      #variable to stop execution

direction = TOP

while execute :

    clock.tick(CLOCK_FREQUENCY)
   
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :   #permet de pouvoir fermer en 
            if event.key == pygame.K_q :        #appuyant sur la touche q
                execute = False 
            if event.key == pygame.K_RIGHT : 
                 direction = RIGHT
            if event.key == pygame.K_LEFT : 
                 direction = LEFT
            if event.key == pygame.K_UP : 
                 direction = TOP
            if event.key == pygame.K_DOWN : 
                 direction = DOWN         
        if event.type == pygame.QUIT :       #en fermant la fenetre
                execute = False
    screen.fill(WHITE)  #remplit en blanc la fenêtre    
    abscisse = 0
    ordonnée = 20
    impair = True
    while abscisse < 400 :
        while ordonnée < 300 :
            rectangle = pygame.Rect(abscisse, ordonnée,SIZE_OF_SQUARE,SIZE_OF_SQUARE)
            ordonnée = ordonnée + 40
            pygame.draw.rect(screen,BLACK,rectangle)
        abscisse = abscisse + 20
        if impair :
            ordonnée = 0
            impair = False
        else : 
            ordonnée = 20
            impair = True
    snake.insert(0,(snake[0][0]+direction[0],snake[0][1]+direction[1]))
    snake.pop()
    for (x,y) in snake :
        rectangle_vert = pygame.Rect(x*SIZE_OF_SQUARE,y*SIZE_OF_SQUARE,SIZE_OF_SQUARE,SIZE_OF_SQUARE)
        pygame.draw.rect(screen,GREEN,rectangle_vert)

    pygame.display.update()

pygame.quit()
quit(0)  # pour sortie en 0 

