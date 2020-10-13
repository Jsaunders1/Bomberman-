

import random, pygame, time

black = (0,0,0)


class Wall(object): #This defines wall as wall as a class so that it can be later used within a tile map
     def __init__(self, wx, wy):
         walls.append(self)
         self.rect = pygame.Rect(wx,wy,40,40)#sets the size and spawn of the wall

class Start(object): #This defines the start point so that no block can spawn here
     def __init__(self, wx, wy):
         starts.append(self)
         self.rect = pygame.Rect(wx,wy,40,40)         

class Brick(object): #This defines the bricks which are destructible spawn power ups
     def __init__(self, wx, wy):
         bricks.append(self)
         self.rect = pygame.Rect(wx,wy,40,40)#sets the size and spawn of the brick

  

class Player1(object): #This allows me to specify my player
     

    def __init__(self):
         self.rect = pygame.Rect(40,40,40,40)
         self.bombs = []#creates an array to prevent overfow of bombs
         self.speed = 5 #sets the start speed for the players
         # Determines the start speed of the players which can then be adjusted by the roller blades power up
         self.bomblim = 2 #sets the start limit for how many bombs can be placed -1.
         self.placed = True #ensures a user cannot place too many bombs
         self.rectangy = [] #creates an array to spawn explosion rectangles
         self.explen = 6 #sets the start size of the bomb explosion
         

    def move(self,dx,dy): #Accepts input to move accordingly 
        if dx!=0:
            self.move_single_axis(dx,0)
        if dy!=0:
            self.move_single_axis(0,dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy  
    
         

 
        for brick in bricks: #Stops the player from passing through the blocks
            if self.rect.colliderect(brick.rect):
                if dx > 0:
                    self.rect.right = brick.rect.left
                if dx < 0:
                    self.rect.left = brick.rect.right
                if dy > 0:
                    self.rect.bottom = brick.rect.top
                if dy < 0:
                    self.rect.top = brick.rect.bottom
                    
        for wall in walls: #Creates collision so that the walls prevent movement through the blocks
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

    def update(self, screen, user_input):
         if user_input[pygame.K_w]: #The relevant input key is taken and follows the given movement 
             self.move(0,-self.speed)
        
        
         if user_input[pygame.K_s]: 
             self.move(0,self.speed)
             

         if user_input[pygame.K_a]:
             self.move(-self.speed,0)
           
             
         if user_input[pygame.K_d]:
             self.move(self.speed,0)
             
             

         if len(self.bombs) < self.bomblim+1:
              if user_input[pygame.K_SPACE] and self.placed == True:
                  x = round(self.rect.x/40)*40 + 20
                  y = round(self.rect.y/40)*40 + 20
                  self.placed = False
                  print len(self.bombs)-1
                  self.bombs.append(bomb((int(x),int(y))))
                  print player1.rect.center
         if user_input[pygame.K_SPACE] == False:
                  self.placed = True
                  
         for b in self.bombs: 
               b.update(screen)
               if b.exploded:
                    self.rectangy.append(blowrectangle((b.pos[0]-20 ,b.pos[1]-20)))
                    for i in range (self.explen):
                         self.rectangy.append(blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20)))
                         self.rectangy.append(blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))
                         self.rectangy.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))
                         self.rectangy.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40))))
                    self.bombs.remove(b)

         for e in self.rectangy:
              e.update(screen)
              if e.end > 3:
                   self.rectangy.remove(e)


              
class blowrectangle(object):
     def __init__ (self,pos):
        self.rect = pygame.Rect((pos),(40,40))
        self.start = time.time()
        self.end = 0
        self.rectangy = []               
               
     def update (self,screen):
        pygame.draw.rect(screen, (0,21,45), (self.rect))
        self.end = time.time() - self.start

class bomb(object): #This defines the bombs
      def __init__(self, pos) :
       self.pos = pos 
       self.start = time.time()
       self.exploded = False
       
      def display(self,screen):
        pygame.draw.circle(screen, black, self.pos,14)
        
        
      def blow(self): #This procedure explodes the bombs
        end = time.time()
        if end - self.start > 3 : #Makes the bombs explodes after 3 seconds
           self.exploded = True

           
           
      def update(self, screen):
           
           self.display(screen)
           self.blow()#Updates the screen to the exploded bomb

class timer(object):
     def __init__(self,pos,fontsize,font):
        self.font = pygame.font.SysFont('Consolas', fontsize, bold=True)
        self.pos = pos
        self.start = 180
        self.mins = 0 
        self.secs = 0
        self.loopcount = 0

     def update(self):
         self.mins = self.start/60
         self.secs = self.start%60
         self.loopcount += 1
         if self.loopcount % 60 == 0:
              self.start -= 1
         if self.secs < 10:
              textsurface = self.font.render(str(self.mins)+':0'+str(self.secs), True , (255,255,255))  
         else: 
              textsurface = self.font.render(str(self.mins)+':'+str(self.secs), True , (255,255,255))
         screen.blit(textsurface,(550,10))
           
        

###parent class power up
           #rectangle box
           #stay unless hit by bomb
           #picked up when touched by player
           
###class extrabomb(object):

###class extendrange(object):

###class rollers(object):

###class kickers(object): cap at 6

     
pygame.init() #This initialises pygame 

#set up display
pygame.display.set_caption("Bomberman V1")#This names the project
width, height = 1160, 760
screen = pygame.display.set_mode((width, height)) #This sets the size of the board to the appopriate, given size
clock = pygame.time.Clock()
Q = 0

walls = []
bricks = []
starts = []
bombs = []
player1 = Player1() #creates a player using the class above
colour = (0,0,0)
black = (0,0,0)




    #This is a tile map which draws the board out on screen.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WS BBBBBBBBBBBBBBBBBBBBBBBBBW",
"W WBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBWBW",
"WBBBBBBBBBBBBBBBBBBBBBBBBBBBW",
"WBWBWBWBWBWBWBWBWBWBWBWBWBW W",
"WBBBBBBBBBBBBBBBBBBBBBBBBB SW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]


x = y = 0
for row in level:
    for col in row:
        if col == "W":    #This reads the tile map as to where to place blocks
            Wall(x,y)
        if col == "S":
            Start(x,y)
        if col == "B":
            Q = random.randint(0,4)  #Gives a 80% chance of bricks spawning                           
            if Q <= 3:
             Brick(x,y)
            
             
        x += 40
    y += 40
    x=0

running = True
gametimer = timer((0,0),24,"arial")

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    user_input = pygame.key.get_pressed() #This controls the player movement 
    
    screen.fill((46,139,87)) # This changes the screen colour
    for start in starts:
         pygame.draw.rect(screen,(255,0,0),start.rect) #Places thet start points
    for brick in bricks:
        pygame.draw.rect(screen,(130,130,130),brick.rect) #Places down the randomized bricks
    for wall in walls:
         pygame.draw.rect(screen,(160,160,160),wall.rect)#Places the walls down in the colour that is given here
         

    
    player1.update(screen, user_input)     
    gametimer.update()
    pygame.draw.rect(screen,colour,player1.rect)
    pygame.display.flip()
    
    

pygame.quit()
quit()
