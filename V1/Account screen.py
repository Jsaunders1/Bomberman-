import pygame
from encryption import hashing

width, height = 1160,760
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
colour_inactive = (30, 30, 30)
colour_active = (255, 255, 255)
FONT = pygame.font.Font(None, 32)


class account(object): 
    def __init__(self, pos, fontsize, font):
        self.font = pygame.font.SysFont('Consolas', 32, bold=True)
        self.pos = pos

    
    def update(self):
        textsurface = self.font.render('Enter username: ', True, (255,255,255)) 
        screen.blit(textsurface, (270,250))
        textsurface = self.font.render('Enter password: ', True, (255,255,255))
        screen.blit(textsurface, (270,350))
        

class login(object):

    def __init__(self, x, y, w, h, text='', store=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour_inactive
        self.font = pygame.font.Font(None, 32)
        self.text = text
        self.store = store
        self.textsurface = FONT.render(text, True, self.colour)
        self.active = False

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE: 
                    self.text = self.text[:-1]
                    self.store = self.store[:-1]
                elif event.key != pygame.K_RETURN:
                    self.store += event.unicode
                    self.text += '*'
                self.textsurface = FONT.render(self.text, True, self.colour)

    def update(self):
        width = max(200, self.textsurface.get_width()+10)
        self.rect.w = width
        self.colour = colour_active if self.active else colour_inactive
        
    def draw(self, screen):    
        screen.blit(self.textsurface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

def checkDetails(username, password):

    try:
        f = open("login.txt", "r")
        lines = f.readlines()
        stored_user = lines[0].strip()
        stored_pass = lines[1].strip()

    except IOError:
        print("Couldn't open login file")
        quit()

    username = hashing(username)
    password = hashing(password)

    if username == stored_user and password == stored_pass: #If user inputs = the stored inputs, then accept the input
        return True
    else:
        return False


running = True
accounts = account((0, 0),32, None)
login1 = login(600, 250, 140, 32)
login2 = login(600, 350, 140, 32)
logins = [login1, login2]
       
while running:
    clock.tick(60)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in logins:
            box.get_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if login1.active:
                    login1.active = False
                    login2.active = True
                elif login2.active:
                    username = login1.store
                    password = login2.store

                    if checkDetails(username, password):
                        from TitleScreen import *
                    else:
                        print('invalid')
                        login1.store = login2.store = ''
                        login1.text = login2.text = ''
                        
    for box in logins:
        box.update()

    
    screen.fill((0,0,0))
    for box in logins:
        box.draw(screen)
            
    
    accounts.update()
    pygame.display.flip()
pygame.quit()
quit()
