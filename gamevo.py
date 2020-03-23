# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 00:31:38 2020

Genetic algo to find a path

Set a random start and stop point and create obstacles in between, must always be random
agents store a string of forces which are vectors and should in theory find a path to end.



@author: Birds
"""
import pygame
import sys, traceback
import gameevo_core as cr


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)



w, h = 600, 400
start = (0,0) # make random in future
end = (500,200)
pop = 5000
mutrate = 0.1
fpg = 700
# user should be able to controle the size of populationa and the time period for each population

sim = cr.sim(w,h,(20,20),end,mutrate,fpg) # controles the entire simulation

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w,h))

sim.obs(12) # put 11 obstacles
sim.initagents(100) # initiate genetic for with 1 agent

def rateupdate(pk,rate):
    if rate < 2:
        rate = 2
    if rate >500:
        rate = 240
    if pk[K_LEFT]:
        rate -= 10
    if pk[K_RIGHT]:
        rate += 10
    return rate
    
on = False
    
rate = 60
try:
    while not on:
        for event in pygame.event.get():
            if event.type == QUIT:
                on = True
        
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    on = True
                
        pk = pygame.key.get_pressed()
        rate = rateupdate(pk,rate)
        screen.fill((240, 255, 240))
        clock.tick(rate)
        pygame.draw.circle(screen,(64,64,255),end,5)
        #don't disturb code above this
        sim.updateall()
        
        # to draw all sprites
        for i in sim.coll:
            screen.blit(i.surf, i.rect)
        for entity in sim.pool:
            pygame.draw.circle(screen, (128, 128, 255), (entity.rect[0] + round(entity.speed.i*2) + 10, entity.rect[1] + round(entity.speed.j*2) + 10), 2)
            screen.blit(entity.surf, entity.rect)         
        pygame.display.flip()
except:
    print("error pls help")
    traceback.print_exc(file=sys.stdout)
finally:    
    pygame.quit()