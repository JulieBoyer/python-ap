import pygame

pygame.init()

BLANC = (255,255,255) #mettre les constantes en majuscule

NOIR = (0,0,0)

WIDTH = 400

HEIGTH = 300

screen = pygame.display.set_mode( (WIDTH, HEIGTH) )

clock = pygame.time.Clock()

CLOCK_FREQUENCY = 1

execute = True      #variable pour permettre fin d'execution

while execute :

    clock.tick(CLOCK_FREQUENCY)
   
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :   #permet de pouvoir fermer en 
            if event.key == pygame.K_q :        #appuyant sur la touche q
                execute = False                    
        if event.type == pygame.QUIT :       #en fermant la fenetre
                execute = False
    screen.fill(BLANC)                  #remplit en blanc la fenêtre    

    pygame.display.update()

pygame.quit()
quit(0)  # pour sortie en 0 

