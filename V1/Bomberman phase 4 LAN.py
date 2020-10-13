
import random, pygame as pg, time #I will require these imports in order for my game to function and work

p1 = pg.image.load("p1.png")#These add in the 4 different power up images to add to my game 
p2 = pg.image.load("p2.png")
p3 = pg.image.load("p3.png")
p4 = pg.image.load("p4.png")
wallblock = pg.image.load("brickblock.png")

class Wall(object): #This defines wall as wall as a class so that it can be later used within a tile map
     def __init__(self, wx, wy):
         walls.append(self)
         self.image = wallblock
         self.rect = pg.Rect(wx,wy,40,40)#sets the size and spawn of the wall

class Start(object): #This defines the start point so that no block can spawn here
     def __init__(self, wx, wy):
         starts.append(self)
         self.rect = pg.Rect(wx,wy,40,40)         

class Brick(object): #This defines the bricks which are destructible spawn power ups
     def __init__(self, wx, wy):
         bricks.append(self)
         self.rect = pg.Rect(wx,wy,40,40)#sets the size and spawn of the brick
  

class Player(object): #This allows me to specify my player
     def __init__(self,x,y,up,down,left,right,place):
          self.rect = pg.Rect(x,y,35,35)
          self.up = up #allows each player to move using different keys
          self.down = down
          self.left = left
          self.right = right
          self.spawnbomb = place #allows each player to place bombs using different keys
          self.bombs = []#creates an array to prevent overfow of bombs
          self.speed = 2 #sets the start speed for the players
          # Determines the start speed of the players which can then be adjusted by the roller blades power up
          self.bomblim = 0 #the start limit for the bombs to be place is 1
          self.placed = True #ensures a user cannot place too many bombs
          self.exploderect = [] #creates an array to spawn explosion rectangles
          self.explen = 3 #sets the start size of the bomb explosion
          self.movable = True #Allows the player to move unless dead
          self.kickers = False #Allows the player to obtain kickers

          


     def move(self,dx,dy): #Accepts input to move accordingly 
          if dx!=0:
               self.move_single_axis(dx,0)
          if dy!=0:
               self.move_single_axis(0,dy)

     def move_single_axis(self, dx, dy):

          self.rect.x += dx
          self.rect.y += dy  
    
         

          for bomb in self.bombs:# Prevents the player from walking back through the bomb once it is placed
              if not self.rect.colliderect(bomb.rect) and bomb.active == False:
                   bomb.active = True 
              if self.rect.colliderect(bomb.rect) and bomb.active:
                   if dx > 0:
                         self.rect.right = bomb.rect.left
                   if dx < 0:
                         self.rect.left = bomb.rect.right
                   if dy > 0:
                         self.rect.bottom = bomb.rect.top
                   if dy < 0:
                         self.rect.top = bomb.rect.bottom

                   if self.kickers:
                        bomb.velX = dx
                        bomb.velY = dy
                   
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
          if self.movable == True: 
              if user_input[self.up]: #The relevant input key is taken and follows the given movement 
                  self.move(0,-self.speed)#Move up
        
        
              if user_input[self.down]: 
                  self.move(0,self.speed) #Move down
             

              if user_input[self.left]:
                  self.move(-self.speed,0) #Move left
           
             
              if user_input[self.right]:
                  self.move(self.speed,0) #Move right
             
             

              if len(self.bombs) < self.bomblim+1: #This ensures the bomb limit cannot be surpassed
                   if user_input[self.spawnbomb] and self.placed == True: #This places the bombs 
                       x = round((self.rect.x + 19)/40)*40 + 20 #These centre the x and y placements of the bomb
                       y = round((self.rect.y + 19)/40)*40 + 20
                       self.placed = False
                       print len(self.bombs)-1
                       self.bombs.append(bomb(int(x),int(y))) #This prints the bomb onto the map
                       print player1.rect.center
              if user_input[self.spawnbomb] == False:
                       self.placed = True
              
          for b in self.bombs:
              for brick in bricks: 
                    if b.rect.colliderect(brick.rect):
                         b.velX = 0
                         b.velY = 0           
              for wall in walls: 
                    if b.rect.colliderect(wall.rect):
                         b.velX = 0
                         b.velY = 0
                                    
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
                                      p = {1: extendbomb((brick.rect.x,brick.rect.y)),
                                           2: extendrange((brick.rect.x,brick.rect.y)),
                                           3: speedboost((brick.rect.x,brick.rect.y)),
                                           4: kickers((brick.rect.x,brick.rect.y))}[random.randint(1,4)]
                                      p.create()
                                      
                             for wall in walls: #prevents explosions traveling through walls
                                 if rectangle.rect.colliderect(wall.rect):
                                      right = False
                                                                                                     
                        if right:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 + ((i+1)*40) ,b.pos[1]-20))) #Keep exploding to the right until the limit if no bricks are touched                                  


                        if left:
                             rectangle = (blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#This explodes the first block to the left to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      left = False
                                      p = {1: extendbomb((brick.rect.x,brick.rect.y)),
                                           2: extendrange((brick.rect.x,brick.rect.y)),
                                           3: speedboost((brick.rect.x,brick.rect.y)),
                                           4: kickers((brick.rect.x,brick.rect.y))}[random.randint(1,4)]
                                      p.create()

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      left = False

                        
                        if left:
                              self.exploderect.append(blowrectangle((b.pos[0]-20 - ((i+1)*40) ,b.pos[1]-20)))#Keep exploding to left until the limit if no bricks are touched


                        if down:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#This explodes the first block to down to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      down = False
                                      p = {1: extendbomb((brick.rect.x,brick.rect.y)),
                                           2: extendrange((brick.rect.x,brick.rect.y)),
                                           3: speedboost((brick.rect.x,brick.rect.y)),
                                           4: kickers((brick.rect.x,brick.rect.y))}[random.randint(1,4)]
                                      p.create()
                                                                              

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      down = False

                                      
                        if down:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 + ((i+1)*40))))#Keep exploding to down until the limit if no bricks are touched


                        if up:
                             rectangle = (blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40))))#This explodes the first block to up to the limit
                             for brick in bricks:
                                 
                                 if rectangle.rect.colliderect(brick.rect): #This removes the bricks when the explosions touch it
                                      bricks.remove(brick)
                                      up = False
                                      p = {1: extendbomb((brick.rect.x,brick.rect.y)),#This selects which powerup will be spawned
                                           2: extendrange((brick.rect.x,brick.rect.y)),
                                           3: speedboost((brick.rect.x,brick.rect.y)),
                                           4: kickers((brick.rect.x,brick.rect.y))}[random.randint(1,4)]
                                      
                                      
                                      p.create() #This creates the powerup with a 1 in 4 chance of spawning

                             for wall in walls:
                                 if rectangle.rect.colliderect(wall.rect):
                                      up = False

                                           
                        if up:
                              self.exploderect.append(blowrectangle((b.pos[0]-20,b.pos[1]-20 - ((i+1)*40)))) #Keep exploding to up until the limit if no bricks are touched


                   self.bombs.remove(b)    

               
          for e in self.exploderect: #if a player collides with the explosion, they can no longer be moved
                if e.rect.colliderect(self.rect):
                     self.movable = False
                e.update(screen,level)

                for bom in self.bombs:
                     if e.rect.colliderect(bom.rect):
                          bom.exploded = True
                     
                if e.end > 1:
                   self.exploderect.remove(e) #this updates the screen to remove the explosions


          for i in range(len(powerups)): #if a player collides with a powerup, they collect it and are given the effect
               if self.rect.colliderect(powerups[i-1].rect):
                    powerups[i-1].apply_effect(self)
                    del powerups[i-1]
               
        




class blowrectangle(object): #Creates a class for spawning the explosions
     def __init__ (self,pos):
        self.rect = pg.Rect((pos),(40,40))
        self.start = time.time()
        self.end = 0
         
     def update (self,screen,level):
       
                       
        pg.draw.rect(screen,(240,162,14), (self.rect)) #draws the recangle with the given colour (0,21,45)
        self.end = time.time() - self.start #Set the time to detect explosion spawn and despawn times




class bomb(object): #This defines the bombs
      def __init__(self, posx, posy) :
       self.pos = (posx,posy)
       self.start = time.time()
       self.exploded = False
       self.rect = pg.Rect((posx-20,posy-20),(30,30))
       self.active = False
       self.velX = 0
       self.velY = 0
       
      def display(self,screen):
        pg.draw.circle(screen, (black), self.pos,15) #Sets the size and colour of the bombs and draws them
        
        
      def blow(self): #This procedure explodes the bombs
        end = time.time()
        if end - self.start > 3 : #Makes the bombs explodes after 3 seconds
           self.exploded = True           
           
      def update(self, screen):
           
           self.display(screen)
           self.rect.x += self.velX
           self.rect.y += self.velY
           self.pos = (self.pos[0] + self.velX, self.pos[1] + self.velY)
           
           self.blow()#Updates the screen to the exploded bomb
           

class timer(object):
     def __init__(self,pos,fontsize,font):
        self.font = pg.font.SysFont('Consolas', fontsize, bold=True) #Chooses a font type and size for the timer
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
              pg.quit()
              quit()           
          

class powerup(object): #creates powerup objects 
     def __init__(self,pos):
          self.rect = pg.Rect((pos),(40,40))
          self.pos = pos
          self.image = p1 
          
          
     def create(self): #gives a 1 in 4 chance of a powerup spawning when a brick is destroyed
          x = random.randint(0,3)
          if x == 0:
               self.spawn = True
               powerups.append(self)

     def update(self,screen):
          pg.draw.rect(screen, (15,5,5),(self.rect))
          screen.blit(self.image,(self.pos))
                         
               

class extendbomb(powerup): #gives the extra bomb powerup properties 
     def __init__(self,pos):
          super(extendbomb,self).__init__(pos)
          self.image = p1

     def apply_effect(self,player):
          if player.bomblim < 7:
               player.bomblim = player.bomblim + 1

     

class extendrange(powerup):#gives the extra range powerup properties 
    def __init__(self,pos):
          super(extendrange,self).__init__(pos)
          self.image = p2
            
    def apply_effect(self, player):
          if player.explen < 7:
               player.explen = player.explen + 1
            
class speedboost(powerup): #gives the extra speed powerup properties 
     def __init__(self,pos):
          super(speedboost,self).__init__(pos)
          self.image = p3               

     def apply_effect(self,player):
          if player.speed < 7:
               player.speed = player.speed + 1

class kickers(powerup): #gives the player the ability to kick bombs
     def __init__(self,pos):
          super(kickers,self).__init__(pos)
          self.image = p4

     def apply_effect(self,player):
          print 'apply effect'
          if player.kickers == False:
               player.kickers = True               

                    
pg.init() #This initialises pg 

#set up display
pg.display.set_caption("Bomberman.")#This names the project
width, height = 1160, 760
screen = pg.display.set_mode((width, height)) #This sets the size of the board to the appopriate, given size
clock = pg.time.Clock()
Q = 0

walls = [] #Creates arrays of all different type of blocks in order to spawn them into the game
bricks = []
starts = []
bombs = []
powerups = [] 
player1 = Player(40,40,pg.K_w,pg.K_s,pg.K_a,pg.K_d,pg.K_SPACE)#creates a player using the class above
player2 = Player(1080,680,pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT,pg.K_RETURN)#Creates a second player using different inputs
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
            Q = random.randint(0,4)  #Gives a 60% chance of bricks spawning                           
            if Q <= 2:
             Brick(x,y)    
        
        x += 40
    y += 40
    x=0

running = True
gametimer = timer((0,0),24,"arial")

while running:
    clock.tick(60) 
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

   
    user_input = pg.key.get_pressed() #This controls the player movement 
    
    screen.fill((46,139,87)) # This changes the screen colour 
    for start in starts:
         pg.draw.rect(screen,(255,0,0),start.rect) #Places thet start points
    for brick in bricks:
        pg.draw.rect(screen,(130,130,130),brick.rect) #Places down the randomized bricks
    for wall in walls:
         screen.blit(wall.image,wall.rect)#Places the walls down in the colour that is given here
    for p in powerups:
         p.update(screen)#updates the screen, allowing powerups to spawn

         
    if (player1.movable == False) and (player2.movable == True):
          font = pg.font.SysFont('Consolas', 32, bold=True)
          texts = font.render("Player 2 Wins", True , (255,255,255))
          screen.blit(texts,(470,340))
          running = False
    if (player1.movable == True) and (player2.movable == False):
          font = pg.font.SysFont('Consolas', 32, bold=True)
          texts = font.render("Player 1 Wins", True , (255,255,255))
          screen.blit(texts,(470,340))
          running = False        
     

    
    player1.update(screen, user_input)
    player2.update(screen, user_input)
    gametimer.update()
    pg.draw.rect(screen,colour,player1.rect)
    pg.draw.rect(screen,colour,player2.rect)
    pg.display.flip()

    
    
time.sleep(5)
pg.quit()
quit()
