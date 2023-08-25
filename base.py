import pygame
import sys

import keyboard
from random import randint



clock = pygame.time.Clock()


screen = pygame.display.set_mode((1200, 800))
bg = pygame.image.load('images/background.png')
pygame.init()


class Object:
    def __init__(self,pos,img):
        self.pos = pos
        self.img = pygame.image.load(img)
    def set_pos(self,new_pos):
        self.pos = new_pos
    def move(self,x,y):
        self.pos = ((self.pos[0]+x if  not self.pos[0]+x > 1180 else 1180) if not self.pos[0]+x < 0 else 0,
                    (self.pos[1] + y if  not self.pos[1] + y > 780 else 780) if not self.pos[1] + y < 0 else 0)
        if self.AnimTrue == True:
            self.img = self.anim[self.anim.index(self.img)+1] if self.anim.index(self.img)+1 != len(self.anim) else self.anim[0] 
    def set_image(self,new_img):
        self.img = pygame.image.load(new_img)
    def set_animation(self,anim):
        self.img = anim[0]
        self.anim = anim
        self.AnimTrue = True

class Enemy:
    def __init__(self):
        self.pos = (0,randint(0,801)) if randint(0,1) == 1 else (1200,randint(0,801))
        self.img = pygame.image.load('images/enemyright.png') #28x18
        self.Bspeed = 3
    def move(self,plpos):
        self.pos = (self.pos[0] + (2 if plpos[0] > self.pos[0] else -2),self.pos[1] + (2 if plpos[1] > self.pos[1] else -2))
        

    def delite():
        #sdfsdfsdfsdfsdfsdfsdfdfdfsdf
        pass


pl = Object((600,600),'images\stop.png')   
pl_anim = [pygame.image.load('images\stop.png'),pygame.image.load('images\down2.png'),pygame.image.load('images\down3.png')]
pl.set_animation(pl_anim)

attackimg_r = pygame.image.load('images/attack_right.png')
attackimg_l = pygame.image.load('images/attack_left.png')
def attackright(pos,img = pygame.image.load('images/attack_right.png')):
    screen.blit(img,(pos[0]+20,pos[1]))
def attackleft(pos,img = pygame.image.load('images/attack_left.png')):
    screen.blit(img,(pos[0]-61,pos[1]))


def lable(txt,pos):
    myfont = pygame.font.Font('NotoSans-Light.ttf',12)
    lable = myfont.render(txt,False,'white','grey')
    screen.blit(lable,pos)


TicsPerSec = 25
attackCD = 0 
attacking = False
enemy_list = [Enemy(),Enemy(),Enemy(),Enemy()]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    screen.blit(bg,(0,0))

    lable(str(pl.pos),(10,10))
    lable(f'score: {0}',(600,10))
    screen.blit(pl.img,pl.pos)
    for i in enemy_list:
        i.move(pl.pos)
        screen.blit(i.img,i.pos)
    if pygame.mouse.get_pressed()[0] and attackCD <= 0:
        attackCD = TicsPerSec
    if attackCD > TicsPerSec//2 :
        if pygame.mouse.get_pos()[0] < pl.pos[0]:
            attackleft(pl.pos)
        else:
            attackright(pl.pos)
    if keyboard.is_pressed('w'):
        pl.move(0, -5)
    if keyboard.is_pressed('s'):
        pl.move(0,5)
    if keyboard.is_pressed('d'):
        pl.move(5, 0)
    if keyboard.is_pressed('a'):
        pl.move(-5, 0)
    pygame.display.update()
    
    attackCD = (attackCD-1) if (attackCD-1) >= 0 else 0 
    clock.tick(TicsPerSec)









