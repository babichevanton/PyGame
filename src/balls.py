#!/usr/bin/env python
# coding: utf

import pygame
import random


SIZE = 640, 480


def intn(*arg):
    return map(int,arg)


def Init(sz):
    '''Turn PyGame on'''
    global screen, screenrect
    pygame.init()
    screen = pygame.display.set_mode(sz)
    screenrect = screen.get_rect()


class GameMode:
    '''Basic game mode class'''
    def __init__(self):
        self.background = pygame.Color("black")

    def Events(self,event):
        '''Event parser'''
        pass

    def Draw(self, screen):
        screen.fill(self.background)

    def Logic(self, screen):
        '''What to calculate'''
        pass

    def Leave(self):
        '''What to do when leaving this mode'''
        pass

    def Init(self):
        '''What to do when entering this mode'''
        pass


class Ball:
    '''Simple ball class'''

    def __init__(self, constants, filename, pos = (0.0, 0.0), speed = (0.0, 0.0), density = 1.0, size = 1.0):
        '''Create a ball from image'''
        self.constants = constants
        self.surface = pygame.image.load(filename)
        new_width = int(round(self.surface.get_width() * size))
        new_height = int(round(self.surface.get_height() * size))
        self.surface = pygame.transform.scale(self.surface, (new_width, new_height))
        self.rect = self.surface.get_rect()
        self.speed = (speed[0] * self.constants['unit'], speed[1] * self.constants['unit'])
        self.pos = (pos[0] * self.constants['unit'], pos[1] * self.constants['unit'])
        self.mass = density * pygame.mask.from_surface(self.surface).count()
        # height =
        # self.energy = self.mass * self.constants['gravity'] *
        self.active = True

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def action(self):
        '''Proceed some action'''
        if self.active:
            self.pos = self.pos[0]+self.speed[0], self.pos[1]+self.speed[1]

    def logic(self, surface):
        x,y = self.pos
        dx, dy = self.speed
        if x < self.rect.width/2:
            x = self.rect.width/2
            dx = -dx
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -dx
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy = -dy
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy = -dy
        self.pos = x,y
        self.speed = dx,dy
        self.rect.center = intn(*self.pos)


class Universe:
    '''Game universe'''

    def __init__(self, grav_acc, unit_int, msec, tickevent = pygame.USEREVENT):
        '''Run a universe with msec tick'''
        self.ga = grav_acc
        self.unit_int = unit_int
        self.msec = msec
        self.tickevent = tickevent

    def get_constants(self):
        constants = {}
        constants['gravity'] = self.ga
        constants['unit'] = self.unit_int
        return constants

    def Start(self):
        '''Start running'''
        pygame.time.set_timer(self.tickevent, self.msec)

    def Finish(self):
        '''Shut down an universe'''
        pygame.time.set_timer(self.tickevent, 0)


class GameWithObjects(GameMode):

    def __init__(self, objects=[]):
        GameMode.__init__(self)
        self.objects = objects

    def locate(self, pos):
        return [obj for obj in self.objects if obj.rect.collidepoint(pos)]

    def Events(self, event):
        GameMode.Events(self, event)
        if event.type == Game.tickevent:
            for obj in self.objects:
                obj.action()

    def Logic(self, surface):
        GameMode.Logic(self, surface)
        for obj in self.objects:
            obj.logic(surface)

    def Draw(self, surface):
        GameMode.Draw(self, surface)
        for obj in self.objects:
            obj.draw(surface)


class GameWithDnD(GameWithObjects):

    def __init__(self, *argp, **argn):
        GameWithObjects.__init__(self, *argp, **argn)
        self.drag = None

    def Events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = self.locate(event.pos)
            if click:
                self.drag = click[0]
                self.drag.active = False
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if self.drag:
                    self.drag.pos = event.pos
                    self.drag.speed = event.rel
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.drag:
                self.drag.active = True
                self.drag = None
        GameWithObjects.Events(self, event)


Init(SIZE)
Game = Universe(9, 5, 50)

Run = GameWithDnD()
for i in xrange(5):
    x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
    dx, dy = 1 + random.random() * 5, 1 + random.random() * 5
    size = 0.5 + 0.5 * random.randrange(3)
    density = 1.0
    Run.objects.append(Ball(Game.get_constants(), "../data/ball.gif", (x,y), (dx,dy), density, size))

Game.Start()
Run.Init()
again = True
while again:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        again = False
    Run.Events(event)
    Run.Logic(screen)
    Run.Draw(screen)
    pygame.display.flip()
Game.Finish()
pygame.quit()
