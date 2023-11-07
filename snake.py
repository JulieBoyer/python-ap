import pygame

pygame.init()

BLANC = (255,255,255) #mettre les constantes en majuscule

NOIR = (0,0,0)

WIDTH = 400

HEIGTH = 300

screen = pygame.display.set_mode( (WIDTH, HEIGTH) )

clock = pygame.time.Clock()

CLOCK_FREQUENCY = 1

while True:

    clock.tick(CLOCK_FREQUENCY)
    screen.fill(BLANC)                  #remplit en blanc la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :   #permet de pouvoir fermer en appuyant sur la touche Q
            if event.key == pygame.K_q :
                pygame.quit()

    pygame.display.update()

