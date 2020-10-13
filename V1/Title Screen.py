import pygame #relevant imports for the screen

home = pygame.image.load("mainscreen.jpg")#loads the three images shown on the main menu
option1 = pygame.image.load("op1.png")
option2 = pygame.image.load("op2.png")
width, height = 1160, 760
screen = pygame.display.set_mode((width, height)) #This sets the size of the board to the appopriate, given size
pygame.init()
clock = pygame.time.Clock()
screen.blit(home, (0,0))


class buttons(object): #Creates clickable options which can be pressed to cause actions
    def __init__(self,screen, pos,image):
        self.pos = pos
        self.image = image
        self.clicked = False
        self.rect = pygame.Rect((pos),(250,210))
        screen.blit(image,(pos))
        

    def action(self, function): #Detects location of cursor to register when buttons are pressed
        cursor = pygame.mouse.get_pos()
        if self.rect.collidepoint(cursor):
            function()


def stop(): #If quit is pressed, closes the game
    pygame.quit()
    quit()

# def play(): #If play is pressed,load the main game
#     from Bomberman.py import *
    
option1 = buttons(screen,(250,210),(pygame.image.load("op1.png"))) #creates a play button
option2 = buttons(screen,(670,210),(pygame.image.load("op2.png"))) #creates a quit button

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is click on a button, do the selected action
            option1.action(play)
            option2.action(stop)
            

    pygame.display.flip()
pygame.quit()
quit()
