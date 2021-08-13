#!/usr/bin/python3
import pygame, sys
from pygame.locals import *
import random, time
 

pygame.init()
 

FPS = 40
FramePerSec = pygame.time.Clock()
 

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
#SCREEN_WIDTH =  1400
#SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SPEED = 25
SCORE = 0


 

score_font = pygame.font.SysFont("Helvetica", 30) 
end_game = pygame.font.SysFont("Helvetica", 50).render("You LOSE LOSER",True, RED)
win_game = pygame.font.SysFont("Helvetica", 50).render("YOU WIN WINNER", True, GREEN)
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((1400,1000))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
#+++++++   GAME OBJECTS ++++++++++
 
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


class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Fire.png')
        self.surf = pygame.Surface((100,100))
        self.rect = self.surf.get_rect(center = (1400 , random.randrange(100,800)))
    def move(self):
        global SCORE
        self.rect.move_ip(-SPEED,0)
        if (self.rect.left < 0):
            SCORE += 1
            self.rect.left -=1
            self.rect.center = (1400,random.randint(40,SCREEN_WIDTH-40))
            

class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dragon.png')
        self.surf = pygame.Surface((201, 300))
        self.rect = self.surf.get_rect(center = (1200, 200))   
       
    def move(self):
        if SCORE%2 == 0:
             self.rect.move_ip(-1,-1)
        else:
             self.rect.move_ip(1,1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('2_entity_000_HURT_001.png')
        self.surf = pygame.Surface((50, 100))
        self.rect = self.surf.get_rect(center = (160, 800))
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,10)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-10, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(10, 0)
        if pressed_keys[K_SPACE]:
             if len(bullets) < 200:  
                 bullets.append(projectile(self.rect.x, self.rect.y, 6, RED, 1))


class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('background.jpg')
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


#+++++++++++++ CREATE GAME OBJECTS ++++++++++++++++++++
enemy_one = Fire()
player_one = Player()
static_dragon = Dragon()
back_ground = Background()
 
fires = pygame.sprite.Group()
fires.add(enemy_one)
fires.add(static_dragon)
all_sprites = pygame.sprite.Group()
all_sprites.add(player_one)
all_sprites.add(enemy_one)
all_sprites.add(static_dragon)

bullets = []
 

 
#+++++++++++++++++  Game Loop  +++++++++++++++++++++++++++++++++++
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

    flag = True

    # for bullet in bullets:
    #     if bullet.x < 1400 and bullet.x > 0:
    #         bullet.x += bullet.vel  
    #         if bullet.x == static_dragon.rect.left  and bullet.y == static_dragon.rect.left :
    #             SCORE += 1
    #             bullets.pop(bullets.index(bullet)) 
                
    #     else:
    #         bullets.pop(bullets.index(bullet)) 
    #         flag = False
   
    for sprite in all_sprites:
        DISPLAYSURF.blit(sprite.image, sprite.rect)
        sprite.move()
        for bullet in bullets:
            if bullet.x < 1400 and bullet.x > 0:
                 bullet.x += bullet.vel  
                 if static_dragon.rect.left == bullet.x and bullet.y <= 250 and bullet.y >= 100:
                     SCORE += 1
                     bullets.pop(bullets.index(bullet)) 
                
            else:
                bullets.pop(bullets.index(bullet)) 
                flag = False
   
        for bullet in bullets:
            bullet.draw(DISPLAYSURF)     
 
    if pygame.sprite.spritecollideany(player_one,fires):
        time.sleep(1.0)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(end_game, (50,300))
        pygame.display.update()
        
        for sprite in all_sprites:
            sprite.kill()
        time.sleep(2.0)
        pygame.quit()
        sys.exit()
    
    if SCORE >= 1000:
        time.sleep(1.0)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(win_game, (50,300))
        for sprite in all_sprites:
            sprite.kill()
        time.sleep(2.0)
        pygame.quit()
        sys.exit()
  
    pygame.display.update()
    FramePerSec.tick(FPS)