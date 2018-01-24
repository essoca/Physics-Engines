#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drawing a circle
"""

import sys, pygame

background_color = (255,255,255)
(width, height) = (320, 240)

class Particle(object):
    def __init__(self, pos, radius):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.color = (0, 0, 255)
        self.thickness = 1

    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.thickness)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Excercise 2')
screen.fill(background_color)

particle = Particle((160, 120), 15)
particle.display()

pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

