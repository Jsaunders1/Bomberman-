import random #These are the imports which I will need to use in my game 
import pygame

class Wall(object): #This defines wall as wall as a class so that it can be later used within a tile map
     def __init__(self, wx, wy):
         walls.append(self)
         self.rect = pygame.Rect(wx,wy,30,30)


class Player(object): #This allows me to specify my player
    def __init__(self):
        self.rect = pygame.Rect(30,30,60,60)

    def move(self,dx,dy): #Accepts input to move accordingly 
        if dx!=0:
            self.move_single_axis(dx,0)
        if dy!=0:
            self.move_single_axis(0,dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy
        

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
        

pygame.init() #This initialises pygame 

#set up display
pygame.display.set_caption("Bomberman V1")#This names the project
width, height = 960, 720
screen = pygame.display.set_mode((width, height)) #This sets the size of the board to the appopriate, given size
clock = pygame.time.Clock()

walls = []
player = Player() #creates a player using the class above
colour = (12,25,0)



    #This is a tile map which draws the board out on screen.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WSS                            W",
"WSS                            W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W                              W",
"W                              W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W                              W",
"W                              W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W                              W",
"W                              W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W                              W",
"W                              W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W  WW  WW  WW  WW  WW  WW  WW  W",
"W                            SSW",
"W                            SSW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]


x = y = 0
for row in level:
    for col in row:
        if col == "W":    #This reads the tile map as to where to place blocks
            Wall(x,y)
        x += 30
    y += 30
    x=0
    
running = True
speed = 5
while running:
    clock.tick(60)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    user_input = pygame.key.get_pressed() #This controls the player movement
    if user_input[pygame.K_LSHIFT]: #Allows an increase in speed by pressing the left shift key
       speed = 10
    else:
       speed = 5
     
    if user_input[pygame.K_w]: #The relevant input key is taken and follows the given movement
        player.move(0,-speed)
   

    if user_input[pygame.K_s]:
        player.move(0,speed)

    if user_input[pygame.K_a]:
        player.move(-speed,0)
      

    if user_input[pygame.K_d]:
        player.move(speed,0)
       

    screen.fill((46,139,87)) # This changes the screen colour

    for wall in walls:
         pygame.draw.rect(screen,(160,160,160),wall.rect)#Places the walls down in the colour that is given here
    pygame.draw.rect(screen,colour,player.rect)
    pygame.display.flip()


pygame.quit()
quit()
