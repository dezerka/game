import pygame
import sys

import keyboard
from random import randint



clock = pygame.time.Clock()


screen = pygame.display.set_mode((1200, 800))
bg = pygame.image.load('images/background.png')
pygame.init()


class Player:
    def __init__(self,img):
        self.img = pygame.image.load(img)
        self.rect= self.img.get_rect()
        self.rect.x = 600
        self.rect.y = 400
    def move(self,x,y):
        self.rect.x = (self.rect.x+x if  not self.rect.x+x > 1180 else 1180) if not self.rect.x+x < 0 else 0
        self.rect.y = (self.rect.y + y if  not self.rect.y + y > 780 else 780) if not self.rect.y + y < 0 else 0
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
        self.img = pygame.image.load('images/enemyright.png') #28x18
        self.rect = self.img.get_rect(topleft=((0,randint(0,801)) if randint(0,1) == 1 else (1200,randint(0,801))))
        self.Bspeed = 3
    def move(self,plpos,forward = 1):
        self.rect.x = self.rect.x + (2*forward if plpos[0] > self.rect.x else -2)
        self.rect.y = self.rect.y + (2*forward if plpos[1] > self.rect.y else -2)


pl = Player('images/stop.png')   
pl_anim = [pygame.image.load('images/stop.png'),pygame.image.load('images/down2.png'),pygame.image.load('images/down3.png')]
pl.set_animation(pl_anim)


class Sword():
    def __init__(self):
        self.attackimg_r = pygame.image.load('images/attack_right.png')
        self.attackimg_l = pygame.image.load('images/attack_left.png')
        self.attack_rect = self.attackimg_r.get_rect()
        self.attack_kd = 0    
    def set_pos(self,cords):
        self.attack_rect.x , self.attack_rect.y = cords
    def timer(self):
        self.attack_kd = (self.attack_kd-1) if (self.attack_kd-1) >= 0 else 0 

weapon = Sword()

def lable(txt,pos):
    myfont = pygame.font.Font('NotoSans-Light.ttf',12)
    lable = myfont.render(txt,False,'white','grey')
    screen.blit(lable,pos)
spawner = 0
Score = 0
TicsPerSec = 25
attackCD = 0 
attacking = False
enemy_list = [Enemy(),Enemy(),Enemy(),Enemy(),Enemy(),Enemy(),Enemy()]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(bg,(0,0))
    lable(str((pl.rect.x,pl.rect.y)),(10,10))
    lable(f'score: {Score}',(600,10))
    screen.blit(pl.img,pl.rect)
    print(pygame.mouse.get_pressed()[0],weapon.attack_kd)
    if pygame.mouse.get_pressed()[0] == True and weapon.attack_kd == 0:
        weapon.attack_kd = TicsPerSec
    if weapon.attack_kd > TicsPerSec/2:
            if pygame.mouse.get_pos()[0] > pl.rect.x:
                weapon.set_pos((pl.rect.x+20,pl.rect.y))
                screen.blit(weapon.attackimg_r,weapon.attack_rect)
            else:
                weapon.set_pos((pl.rect.x-62,pl.rect.y))
                screen.blit(weapon.attackimg_l,weapon.attack_rect)
    elif weapon.attack_kd <= TicsPerSec/2:
        weapon.set_pos((10000000,10000000))
    for enemy in enemy_list:
        enemy.move((pl.rect.x,pl.rect.y)) #enemy
        indx = enemy_list.index(enemy)
        redacted_enemy_list = list(map(lambda a: a.rect,enemy_list[:indx]))+list(map(lambda a: a.rect,enemy_list[indx+1:]))
        for j in redacted_enemy_list:
            if enemy.rect.colliderect(j):
                enemy.move((j.x,j.y),forward= -2)
        screen.blit(enemy.img,enemy.rect)
    for e in enemy_list:
        if e.rect.colliderect(weapon.attack_rect):
            enemy_list.pop(enemy_list.index(e))
            Score += 1
    if keyboard.is_pressed('w'):
        pl.move(0, -5)
    if keyboard.is_pressed('s'):
        pl.move(0,5)
    if keyboard.is_pressed('d'):
        pl.move(5, 0)
    if keyboard.is_pressed('a'):
        pl.move(-5, 0)
    pygame.display.update()
    for i in enemy_list:
        if pl.rect.colliderect(i) == True:
            enemy_list = []
            pl.rect.x = 600
            pl.rect.y = 400
            Score = 0
    if spawner == 10:
        enemy_list.append(Enemy())
        spawner = 0
    else:
        spawner += 1
    weapon.timer()
    clock.tick(TicsPerSec)









