
import random, pygame, time #I will require these imports in order for my game to function and work

p1 = pygame.image.load("p1.png")#These add in the 4 different power up images to add to my game
p2 = pygame.image.load("p2.png")
p3 = pygame.image.load("p3.png")
p4 = pygame.image.load("p4.png")


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

  

class Player(object): #This allows me to specify my player
     

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


                   


class Player1(Player): #This allows me to specify my player
    def __init__(self):
        self.rect = pygame.Rect(40,40,38,38)
        self.bombs = []#creates an array to prevent overfow of bombs
        self.speed = 3 #sets the start speed for the players
        # Determines the start speed of the players which can then be adjusted by the roller blades power up
        self.bomblim = 1 #the start limit for the bombs to be place is 1
        self.placed = True #ensures a user cannot place too many bombs
        self.exploderect = [] #creates an array to spawn explosion rectangles
        self.explen = 3 #sets the start size of the bomb explosion
        self.movable = True #Allows the player to move unless dead
      #  self.image = pygame.image.load()#Set the start player image
       # self.d_image = pygame.image.load()#Sets the dead player image

    def update(self, screen, user_input):
         if self.movable == True: 
              if user_input[pygame.K_w]: #The relevant input key is taken and follows the given movement 
                  self.move(0,-self.speed)#Move up
        
        
              if user_input[pygame.K_s]: 
                  self.move(0,self.speed) #Move down
             

              if user_input[pygame.K_a]:
                  self.move(-self.speed,0) #Move left
           
             
              if user_input[pygame.K_d]:
                  self.move(self.speed,0) #Move right
             
             

         if len(self.bombs) < self.bomblim+1: #This ensures the bomb limit cannot be surpassed
              if user_input[pygame.K_SPACE] and self.placed == True: #This places the bombs 
                  x = round((self.rect.x + 19)/40)*40 + 20 #These centre the x and y placements of the bomb
                  y = round((self.rect.y + 19)/40)*40 + 20
                  self.placed = False
                  print len(self.bombs)-1
                  self.bombs.append(bomb((int(x),int(y)))) #This prints the bomb onto the map
                  print player1.rect.center
         if user_input[pygame.K_SPACE] == False:
                  self.placed = True

           
         for b in self.bombs:
              up = True
              down = True
              left = True
              right = True
              b.update(screen)
              if b.exploded: #This shows the bomb explosions
                   self.exploderect.append(blowrectangle((b.pos[0]-20 ,b.pos[1]-20))) #This places the centre part of the explosion
                   for i in range (self.explen):
                        if right:
                             rectangle = (blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20))) #This explodes the first block to the right to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      right = False
                                      p = powerup(((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20)))
                                      p.choice()
                                      
                             for wall in walls: #prevents explosions traveling through walls
                                 if rectangle.rect.colliderect(wall.rect):
                                      right = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False                                                                  
 

                                  
                        if right:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20))) #Keep exploding to the right until the limit if no bricks are touched                                  

                        if left:
                             rectangle = (blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#This explodes the first block to the left to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      left = False
                                      p = powerup(((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))
                                      p.choice()

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      left = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False  
                            
                        if left:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#Keep exploding to left until the limit if no bricks are touched

                        if down:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#This explodes the first block to down to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      down = False
                                      p = powerup((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40)))
                                      p.choice()
                                                                              

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      down = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False
                                      
                        if down:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#Keep exploding to down until the limit if no bricks are touched

                        if up:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40))))#This explodes the first block to up to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      up = False
                                      p = powerup((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40)))
                                      p.choice()

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      up = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False
                                           
                        if up:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40)))) #Keep exploding to up until the limit if no bricks are touched    
                          
                   self.bombs.remove(b)
         for e in self.exploderect: 
                e.update(screen,level)
                if e.end > 1:
                   self.exploderect.remove(e) #this updates the screen to remove the explosions
     

     

class Player2(Player):
       def __init__(self):
         self.rect = pygame.Rect(1080,680,38,38)
         self.bombs = []#creates an array to prevent overfow of bombs
         self.speed = 3 #sets the start speed for the players
         # Determines the start speed of the players which can then be adjusted by the roller blades power up
         self.bomblim = 1 #the start limit for the bombs to be place is 1
         self.placed = True #ensures a user cannot place too many bombs
         self.exploderect = [] #creates an array to spawn explosion rectangles
         self.explen = 3 #sets the start size of the bomb explosion
         self.movable = True #Allows the player to move unless dead
      #  self.image = pygame.image.load()#Set the start player image
       # self.d_image = pygame.image.load()#Sets the dead player image
     
       def update(self, screen, user_input):
         if self.movable == True: 
              if user_input[pygame.K_UP]: #The relevant input key is taken and follows the given movement 
                  self.move(0,-self.speed)#Move up
        
        
              if user_input[pygame.K_DOWN]: 
                  self.move(0,self.speed) #Move down
             

              if user_input[pygame.K_LEFT]:
                  self.move(-self.speed,0) #Move left
           
             
              if user_input[pygame.K_RIGHT]:
                  self.move(self.speed,0) #Move right
             
             

         if len(self.bombs) < self.bomblim+1: #This ensures the bomb limit cannot be surpassed
              if user_input[pygame.K_RETURN] and self.placed == True: #This places the bombs 
                  x = round((self.rect.x + 19)/40)*40 + 20 #These centre the x and y placements of the bomb
                  y = round((self.rect.y + 19)/40)*40 + 20
                  self.placed = False
                  print len(self.bombs)-1
                  self.bombs.append(bomb((int(x),int(y)))) #This prints the bomb onto the map
                  print player1.rect.center
         if user_input[pygame.K_RETURN] == False:
                  self.placed = True

           
         for b in self.bombs:
              up = True
              down = True
              left = True
              right = True
              b.update(screen)
              if b.exploded: #This shows the bomb explosions
                   self.exploderect.append(blowrectangle((b.pos[0]-20 ,b.pos[1]-20))) #This places the centre part of the explosion
                   for i in range (self.explen):
                        if right:
                             rectangle = (blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20))) #This explodes the first block to the right to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      right = False
                                      p = powerup(((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20)))
                                      p.choice()
                                      
                             for wall in walls: #prevents explosions traveling through walls
                                 if rectangle.rect.colliderect(wall.rect):
                                      right = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False                                                                  
 

                                  
                        if right:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20))) #Keep exploding to the right until the limit if no bricks are touched                                  

                        if left:
                             rectangle = (blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#This explodes the first block to the left to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      left = False
                                      p = powerup(((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))
                                      p.choice()

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      left = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False  
                            
                        if left:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#Keep exploding to left until the limit if no bricks are touched

                        if down:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#This explodes the first block to down to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      down = False
                                      p = powerup((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40)))
                                      p.choice()
                                                                              

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      down = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False
                                      
                        if down:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#Keep exploding to down until the limit if no bricks are touched

                        if up:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40))))#This explodes the first block to up to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      up = False
                                      p = powerup((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40)))
                                      p.choice()

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      up = False

#                             if rectangle.rect.colliderect(bomb.rect):
 #                                bomb.exploded = True

                             if rectangle.rect.colliderect(self.rect):
                                 self.movable = False
                                           
                        if up:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40)))) #Keep exploding to up until the limit if no bricks are touched    
                          
                   self.bombs.remove(b)

         for e in self.exploderect: 
                e.update(screen,level)
                if e.end > 1:
                   self.exploderect.remove(e) #this updates the screen to remove the explosions




class blowrectangle(object): #Creates a class for spawning the explosions
     def __init__ (self,pos):
        self.rect = pygame.Rect((pos),(40,40))
        self.start = time.time()
        self.end = 0
         
     def update (self,screen,level):
       
                       
        pygame.draw.rect(screen, (0,21,45), (self.rect)) #draws the recangle with the given colour (0,21,45)
        self.end = time.time() - self.start #Set the time to detect explosion spawn and despawn times




class bomb(object): #This defines the bombs
      def __init__(self, pos) :
       self.pos = pos 
       self.start = time.time()
       self.exploded = False
       
      def display(self,screen):
        pygame.draw.circle(screen, (black), self.pos,14) #Sets the size and colour of the bombs and draws them
        
        
      def blow(self): #This procedure explodes the bombs
        end = time.time()
        if end - self.start > 3 : #Makes the bombs explodes after 3 seconds
           self.exploded = True

           
           
      def update(self, screen):
           
           self.display(screen)
           self.blow()#Updates the screen to the exploded bomb

class timer(object):
     def __init__(self,pos,fontsize,font):
        self.font = pygame.font.SysFont('Consolas', fontsize, bold=True) #Chooses a font type and size for the timer
        self.pos = pos
        self.start = 180
        self.mins = 0 
        self.secs = 0
        self.loopcount = 0

     def update(self):
         self.mins = self.start/60 #Starts the count of the minutes and seconds
         self.secs = self.start%60
         self.loopcount += 1
         if self.loopcount % 60 == 0:
              self.start -= 1
         if self.secs < 10:
              textsurface = self.font.render(str(self.mins)+':0'+str(self.secs), True , (255,255,255)) #ensures a 0 is shown before single digit seconds  
         else: 
              textsurface = self.font.render(str(self.mins)+':'+str(self.secs), True , (255,255,255)) #Places a : between minutes and seconds
         screen.blit(textsurface,(550,10)) #Places the timer on the screen
         if (self.mins == 0) and (self.secs == 0): ## If timer reaches 0, close the program
              pygame.quit()
              quit()           
          

class powerup(object):
     def __init__(self,pos):
          self.rect = pygame.Rect((pos),(40,40))
          self.pos = pos
          
     def choice(self):
         x = random.randint(0,3)
         if x == 0:
             self.spawn = True
             powerups.append(self)

     def update(screen):
          for p in powerups:
               if player.rect.colliderect(powerup.rect):
                    a = random.randint(0,5)
                    if a == (0 or 1):
                         extendbomb.spawn
                         b = p1
                    if a == (2 or 3):
                         extendrange.spawn
                         b = p2
                    if a == 4:
                         speedboost.spawn
           #         if a == 5:
            #             kickers.spawn

                         
               

class extendbomb(powerup):
     def __init__(self,pos):
          powerup.rect = pygame.Rect((pos),(40,40))
          powerup.pos = pos

     def spawn(self,screen):
          if Player1.bomblim < 7:
               Player1.bomblim = Player1.bomblim + 1
               pygame.draw.rect(screen, (15,5,5),(self.rect))
               screen.blit(p1,(p.pos))

class extendrange(powerup):
     def __init__(self,pos):
          powerup.rect = pygame.Rect((pos),(40,40))
          powerup.pos = pos

     def spawn(self,screen):
          if Player.explen < 7:
               Player.explen = Player.explen + 1
               pygame.draw.rect(screen, (15,5,5),(self.rect))
               screen.blit(p1,(p.pos))

               
class speedboost(powerup):
     def __init__(self,pos):
          powerup.rect = pygame.Rect((pos),(40,40))
          powerup.pos = pos

     def spawn(self, screen):
          if Player.speed < 7:
               Player.speeed = Player.speed + 1
               pygame.draw.rect(screen, (15,5,5),(self.rect))
               screen.blit(p1,(p.pos))

#class kickers(powerup):
#     def __init__(self,pos):
#          powerup.rect = pygame.Rect((pos),(40,40))
#          powerup.pos = pos
#
#     def spawn(self):
#          if Player.kickers == False
               
               
               
         


     
pygame.init() #This initialises pygame 

#set up display
pygame.display.set_caption("Bomberman.")#This names the project
width, height = 1160, 760
screen = pygame.display.set_mode((width, height)) #This sets the size of the board to the appopriate, given size
clock = pygame.time.Clock()
Q = 0

walls = [] #Creates arrays of all different type of blocks in order to spawn them into the game
bricks = []
starts = []
bombs = []
powerups = [] 
player1 = Player1()#creates a player using the class above
player2 = Player2()
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

#    if Player1.movable == False and Player2.movable == True:
 #        pygame.display.flip()
   
    user_input = pygame.key.get_pressed() #This controls the player movement 
    
    screen.fill((46,139,87)) # This changes the screen colour 
    for start in starts:
         pygame.draw.rect(screen,(255,0,0),start.rect) #Places thet start points
    for brick in bricks:
        pygame.draw.rect(screen,(130,130,130),brick.rect) #Places down the randomized bricks
    for wall in walls:
         pygame.draw.rect(screen,(160,160,160),wall.rect)#Places the walls down in the colour that is given here
    for p in powerups:
         screen.blit(p3,(p.pos))

         
         

    
    player1.update(screen, user_input)
    player2.update(screen, user_input)
    gametimer.update()
    pygame.draw.rect(screen,colour,player1.rect)
    pygame.draw.rect(screen,colour,player2.rect)
    pygame.display.flip()
    
    

pygame.quit()
quit()
