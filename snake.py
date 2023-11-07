import pygame

pygame.init()

blanc = (255,255,255)

width = 400

heigth = 300

screen = pygame.display.set_mode( (width, heigth) )

clock = pygame.time.Clock()

clock_frequency = 1

while True:

    clock.tick(clock_frequency)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q :
                pygame.quit()

    screen.fill(blanc)

    pygame.display.update()

