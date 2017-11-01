import pygame, os, sys
from pygame.locals import *

############################################
# Window initialization + global variables #
############################################
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()
clock = pygame.time.Clock()
pygame.display.set_caption("Saboteur")

black = (0, 0, 0)
pink = (255, 132, 188)
b = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()
    if b:
        screen.fill(pink)
    else:
        screen.fill(black)
    b = not b
    pygame.display.update()
    clock.tick(1)

def wait():
    while 1:
        ''' Pause Until Input is Given '''
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN:
            break

# this calls the 'main' function when this script is executed
# if __name__ == '__main__':
#    main()
