#!/usr/bin/python3
import pygame, sys
from pygame.locals import *
import random, time
 

pygame.init()
 

FPS = 60
FramePerSec = pygame.time.Clock()
 

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH =  800
SCREEN_HEIGHT = 1000
SPEED = 5
SCORE = 0
 

 

score_font = pygame.font.SysFont("Helvetica", 30) 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((800,1000))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 

 
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('resize-1628720171511849972fish.png')
        self.surf = pygame.Surface((100,100))
        self.rect = self.surf.get_rect(center = (800 , random.randrange(100,900)))
    def move(self):
        global SCORE
        self.rect.move_ip(-SPEED,0)
        if (self.rect.left < 100):
            SCORE += 1
            self.rect.left = 0
            self.rect.center = (800,random.randint(40,SCREEN_WIDTH-40))
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('resize-16287173771310531498croppedimage1.png')
        self.surf = pygame.Surface((40, 250))
        self.rect = self.surf.get_rect(center = (160, 900))
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
             if len(bullets) < 5:  
                 bullets.append(projectile(self.rect.x, self.rect.y, 6, (0,0,0), 1))


class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('resize-1628716869767050011325624a61782e94.jpg')
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width
 
            self.moving_speed = 5
         
      def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
             
      def render(self):
         DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
         DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

enemy_one = Fish()
player_one = Player()
back_ground = Background()
 
fishes = pygame.sprite.Group()
fishes.add(enemy_one)
all_sprites = pygame.sprite.Group()
all_sprites.add(player_one)
all_sprites.add(enemy_one)

bullets = []
 

 
#Game Loop
while True:
       
    #Cycles through all occurring events   
    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
 
    back_ground.update()
    back_ground.render()
 
     #after I render the game I can start manipulating the score i think
    score = score_font.render("score: " + str(SCORE), True, RED)
    DISPLAYSURF.blit(score, (25,25))


    for bullet in bullets:
        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel  
        else:
            bullets.pop(bullets.index(bullet)) 
       
   
    for sprite in all_sprites:
        DISPLAYSURF.blit(sprite.image, sprite.rect)
        sprite.move()
        for bullet in bullets:
            bullet.draw(DISPLAYSURF)     
    pygame.display.update()
    FramePerSec.tick(FPS)