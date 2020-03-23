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
w, h = 600, 400

# Start and End Points
start = (0, 0)
end = (500, 200)

# population per gen., mutation rate, frames given to each gen., No. of obs
pop = 50
mutrate = 0.2
fpg = 700
obs = 5

# initializing a sim object
sim = cr.sim(w, h, (50, 50), end, mutrate, fpg)

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
    if rate_ < 30:
        rate_ = 30
    if rate_ > 500:
        rate = 480
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
        clock.tick(rate)
        
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
            pygame.draw.circle(screen, (128, 255, 128),
                               (entity.rect[0] + round(entity.speed.i*2) + 10,
                                entity.rect[1] + round(entity.speed.j*2) + 10),
                               2)
            screen.blit(entity.surf, entity.rect)
            
        pygame.display.flip()
except:
    print("error pls help")
    traceback.print_exc(file=sys.stdout)
finally:
    pygame.quit()
