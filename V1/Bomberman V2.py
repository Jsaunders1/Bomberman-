

import random, pygame, time

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
         self.bombs = []
         self.speed = 1
         # Determines the start speed of the players which can then be adjusted by the roller blades power up
         self.bomblim = 0
         self.placed = True
         
     

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
                    self.bombs.remove(b)
                 #60,60 
             

black = (0,0,0)

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
           
        

###parent class power up
           #rectangle box
           #stay unless hit by bomb
           #picked up when touched by player
           
###class extrabomb(object):

###class extendrange(object):

###class rollers(object):

###class kickers(object):

     
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
            Q = random.randint(0,4)  #Gives a 75% chance of bombs spawning                           
            if Q <= 3:
             Brick(x,y)
          
        x += 40
    y += 40
    x=0
    
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    user_input = pygame.key.get_pressed() #This controls the player movement 
    
    screen.fill((46,139,87)) # This changes the screen colour               
    for start in starts:
         pygame.draw.rect(screen,(0,51,0),start.rect) #Places thet start points

    for brick in bricks:
        pygame.draw.rect(screen,(130,130,130),brick.rect) #Places down the randomized bricks
    for wall in walls:
         pygame.draw.rect(screen,(160,160,160),wall.rect)#Places the walls down in the colour that is given here

    
    player1.update(screen, user_input)     
    pygame.draw.rect(screen,colour,player1.rect)
    pygame.display.flip()


pygame.quit()
quit()
