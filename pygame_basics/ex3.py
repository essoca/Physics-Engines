#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Move the circle
"""
import sys, pygame
import math

background_color = (255,255,255)
(width, height) = (320, 240)

class Particle(object):
    def __init__(self, pos, radius):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.color = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)
        
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed    

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Excercise 3')

particle = Particle((160, 120), 15)
particle.speed = 0.5
particle.angle = 0.25*math.pi

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.fill(background_color)
    particle.move()
    if particle.x > 320 or particle.y < 0:
        particle.x, particle.y = 0, 240
    particle.display()
    pygame.display.flip()
    pygame.time.delay(10)

