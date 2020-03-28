# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 02:03:11 2020

@author: Birds

#game evo classes
"""




import pygame
import random
import numpy as np

class vector(): # simple vector class defines vectors in a polar system
    def __init__(self, i = None, j = None):
        if i != None :
            self.i = i
        else:
            self.i = random.randrange(-1, 2) *0.01

        if j != None :
            self.j = j
        else:
            self.j = random.randrange(-1, 2) *0.01

    def add(self,that):
        self.i+= that.i
        self.j+= that.j

    def sub(self,that):
        self.i-= that.i
        self.j-= that.j

    def cc(self,c , m =1):
        self.i = c.i * m
        self.j = c.j * m

    def mag(self):
        return ((self.i)**2 +(self.j)**2)**0.5
    
    def show2(self):
        return (self.i,self.j)

    def show(self):
        print(self.i,"i-> + ", self.j, "j->",sep="")

class box(pygame.sprite.Sprite): # to make boxes of different colors
    def __init__(self, pos, size):
        super(box, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((random.randint(69,87),random.randint(98,123), random.randint(128,255)))
        self.rect = self.surf.get_rect(center = (pos))

class agent(pygame.sprite.Sprite):

    def __init__(self, start,lifespan,forces = []):
        super(agent, self).__init__()
        self.surf = pygame.Surface((6,6))
        self.surf.fill((100, 100, 45))
        self.rect = self.surf.get_rect(center = (start.show2())) # fix center of box to not intersect with edges of plane

        self.xandy = vector(0,0)
        self.speed = vector(0,0)
        self.acc = vector(0,0)
        self.score = 1 #@TODO calculate score
        self.lifespan = lifespan
        self.inblock = 0
        self.path = []
        self.highpoint = (0,0)

        if len(forces) == 0:
            self.forces = np.array([])
            for _ in range(self.lifespan):
                temp = vector()
                self.forces = np.append(self.forces, temp)
        else:
            self.forces = np.array(forces)

    def update(self,now):
        if(now < self.lifespan):
            self.acc.add(self.forces[now])
        else:
            self.acc.cc(self.acc,0)
        if now % 5 == 4:
            self.path.append((self.rect.x, self.rect.y))
            
        self.speed.add(self.acc)

        # self.surf.fill((0,0,125),self.rect)

        self.xandy.i = self.rect.x
        self.xandy.j = self.rect.y

        self.rect.move_ip(self.speed.i,self.speed.j)



class sim():
    def __init__(self,w,h,start,end,mutrate,fpg):
        self.w = w
        self.h = h
        self.lifespan = fpg
        self.start = vector(start[0], start[1])
        self.end = vector(end[0],end[1])
        self.gr = pygame.sprite.Group()
        self.pool = pygame.sprite.Group()
        self.coll = pygame.sprite.Group()
        self.mutrate = mutrate # take from user
        self.now = -1 # del later for testing only
        self.maxscore = 0
        self.best = [(0,0),(10,10)]
        self.highpoint = (0,0)
        for i in range(fpg):
            self.maxscore+=i

    def colcalc(self,agentcol): # pending redo with scoring system
        
        if self.now < agentcol.lifespan :
            argu = agentcol.score/self.lifespan* 3 * 255
            if argu > 255:
                argu = 255
            if argu < 0:
                argu = 50
            col = (argu/2,argu,argu/2)
        else:
            col = (158,64,64) # color for a dead agent
        return col

    def breed(self, this, that):
        pivot = random.randint(0,self.lifespan)
        # pivot = round(self.lifespan/2)
        forces = np.array([])
        for i in range(pivot):
            if random.random() < self.mutrate:
                temp = vector(0,0)
                this.forces[i] = temp
            forces = np.append(forces,this.forces[i])
        for i in range(pivot, self.lifespan):
            if random.random() < self.mutrate:
                that.forces[i] = vector()
            forces = np.append(forces,that.forces[i])
            
        return agent(self.start,self.lifespan,forces)
    
    # make score func
    def score(self,entity):
        # score is calculated every time period, if higher it is updated warna nahi. time inverse is multiplied with score to prefer thoes who reached end first
        distance = vector(0,0)
        distance.cc(self.start)
        distance.sub(self.end)
        distance.mag() # max distance there could be
        temp = vector(0,0)
        temp.cc(self.end)
        temp.sub(entity.xandy)
        at = temp.mag()
        scorenow = (1-(at/distance.mag())) *100 + (1- ((self.now/self.lifespan))) * 100
        if scorenow < 0:
            scorenow = 0
        if entity.score < scorenow:
            entity.highpoint = (entity.rect.x, entity.rect.y)
            entity.score = scorenow
    
    def selection(self,tempholder):
        '''
        choice = random.random()
        for i in tempholder:
            if choice < i.score:
                return i
        '''
        index = random.randint(0,11)
        return tempholder[index]

    def reset(self):
        tempholder = self.pool.sprites()
        tempholder = sorted(tempholder, key = lambda x : x.score, reverse = True)
        self.best = tempholder[0].path
        self.highpoint = tempholder[0].highpoint
        sumall = 0
        for i in tempholder:
            sumall += i.score
        print(tempholder[0].score)
        tempholder[0].score /= sumall
        print(tempholder[0].score)
        for i in range(1,len(tempholder)):
            tempholder[i].score /= sumall
            tempholder[i].score += tempholder[i-1].score
        
        for i in self.pool :
            one = self.selection(tempholder)
            two = self.selection(tempholder)
        
            if one == two : 
                one = self.selection(tempholder)
            i.kill()
            self.addagent(self.breed(one,two))
        



    def updateall(self):
        if self.now == self.lifespan:
            self.now = -1
            self.reset()
        self.now += 1
        stoplist = []
        for block in self.coll:
            temp = pygame.sprite.spritecollide(block,self.pool,False)
            for _ in temp:
                stoplist.append(_)

        for entity in self.pool:

            if entity in stoplist:
                if entity.inblock == 0:
                    entity.inblock = 1
                    entity.speed.cc(entity.speed,-0.8)
            else:
                entity.inblock = 0


            entity.update(self.now)
            self.score(entity)
            entity.surf.fill(self.colcalc(entity))
            # print(entity.score)
            
            if entity.rect.left < 0 :
                entity.rect.left = 0
                entity.speed.cc(entity.speed,0.8)

            if entity.rect.right > self.w:
                entity.speed.cc(entity.speed,0.8)
                entity.rect.right = self.w

            if entity.rect.top < 0:
                entity.rect.top = 0
                entity.speed.cc(entity.speed,0.8)

            if entity.rect.bottom > self.h:
                entity.rect.bottom = self.h
                entity.speed.cc(entity.speed,0.8)

            """
            # the infinte screen code
            
            if entity.rect.left > self.w :
                entity.rect.left = 0

            if entity.rect.right < 0:
                entity.rect.right = self.w

            if entity.rect.top > self.h:
                entity.rect.top = 0

            if entity.rect.bottom < 0:
                entity.rect.bottom = self.h
            """

    def initagents(self, pop):
        for _ in range(pop):
            temp = agent(self.start,self.lifespan)
            self.addagent(temp)
            
    def addagent(self,temp):
        self.pool.add(temp)
        self.gr.add(temp)
    def addcoll(self, box):
        self.coll.add(box)
        self.gr.add(box)

    # func to gen obstacles TODO: Make sure they are between start and end
    def obs(self,x):
     for _ in range(x):
         A = random.randint( 10, self.w/2)  # two consts to make code readable
         B = random.randint( 10, self.h/2)
         pos = (random.randint((self.w/2) - A,(self.w/2) + A), random.randint((self.h/2) - B, (self.h/2) + B))
         size = (random.randint(10, self.w - pos[0])//2, random.randint(2, self.h - pos[1])//2)
         tmp = box(pos,size)
         self.addcoll(tmp);

def unittest():
    # ob = sim(600,400,(10,10),(300,200))
    # print(dir(ob.pool))

    print("works")

# unittest()

