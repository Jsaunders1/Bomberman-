import pygame #relevant imports for screen

width, height = 1160,760 #sets screen size 
pygame.init() #initialises pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))


pygame.print "hello"

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()
pygame.quit()
quit()
