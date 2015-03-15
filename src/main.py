#!/usr/bin/env python
# coding: utf

import pygame
import random

from gameuniverse import Universe
from gamemode import GameWithDnD
from gameobjects import Ball


SIZE = 640, 480


def Init(sz):
    '''Turn PyGame on'''
    global screen, screenrect
    pygame.init()
    screen = pygame.display.set_mode(sz)
    pygame.display.set_caption("Python Balls")
    screenrect = screen.get_rect()


Init(SIZE)
Game = Universe(50, 0.1, 20)

Run = GameWithDnD()
for i in xrange(1):
    x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
    dx, dy = 1 + random.random() * 5, 1 + random.random() * 5
    angle_speed = 10 - random.randrange(21)
    size = 0.5 + 0.5 * random.randrange(3)
    density = 1.0
    Run.objects.append(Ball(Game.get_constants(), "../data/ball.gif", (x,y), (dx,dy), angle_speed, density, size))

Game.Start()
Run.Init()
again = True
while again:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        again = False
    Run.Events(event, Game.get_possible_events())
    Run.Logic(screen)
    Run.Draw(screen)
    pygame.display.flip()
Game.Finish()
pygame.quit()
