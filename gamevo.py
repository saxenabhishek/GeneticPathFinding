# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 00:31:38 2020

Genetic algo to find a path

Set a random start and stop point and create obstacles in between, must always be random
agents store a string of forces which are vectors and should in theory find a path to end.


@author: Birds
"""
import sys
import traceback
import pygame
import gameevo_core as cr


from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

## Global variables to controle things

# height and width of the window
w, h = 1280, 600

# Start and End Points
start = (20, 20)
end = (1100, 500)

# population per gen., mutation rate, frames given to each gen., No. of obs
pop = 200
mutrate = 0.01
fpg = 300
obs = 15

# initializing a sim object
sim = cr.sim(w, h, start, end, mutrate, fpg)

# pygame initializations
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))

# tells sim about obs and population to put
sim.obs(obs)
sim.initagents(pop)

def rateupdate(pk_, rate_):
    """
    when you press the arrow keys this function changes the framerate
    """
    if rate_ < 2:
        rate_ = 2
    if rate_ > 420:
        rate_ = 420
    if pk_[K_LEFT]:
        rate_ -= 10
    if pk_[K_RIGHT]:
        rate_ += 10
    return rate_

# to know if you are still intrested and if so whats the framerate
on = False
rate = 60

# try block because pygame messesup bigtime
try:
    # game loop
    while not on:
        # if you feel like quiting
        for event in pygame.event.get():
            if event.type == QUIT:
                on = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    on = True
        pk = pygame.key.get_pressed()
        rate = rateupdate(pk, rate)
        screen.fill((50, 50, 80))
        #clock.tick(rate)
        # Blue circle for end point
        pygame.draw.circle(screen, (64, 64, 255), end, 5)
        #don't disturb code above this
        
        # update everything
        sim.updateall()
        
        # to draw all sprites
        for i in sim.coll:
            screen.blit(i.surf, i.rect)
            
        for entity in sim.pool:
            
            # draw cicles to know velocity direction
            screen.blit(entity.surf, entity.rect)
            
            cirpos = (entity.rect[0] + round(entity.speed.i * 5),
                      entity.rect[1] + round(entity.speed.j * 5))
            
            pygame.draw.aaline(screen,(170, 160, 128),
                               (entity.rect[0] + 3, entity.rect[1] + 3),
                               cirpos,1)
            pygame.draw.circle(screen, (128, 255, 128),cirpos,2)
            
        #draw best path from last gen
        pygame.draw.lines(screen,(128,200,128),False,sim.best,2)
        #draw cicle on best path to show the highest point on it
        pygame.draw.circle(screen,(255,128,100),sim.highpoint,5)
        
        pygame.display.flip()
except:
    print("error pls help")
    traceback.print_exc(file=sys.stdout)
finally:
    pygame.quit()
