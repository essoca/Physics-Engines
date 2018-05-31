#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Play basketball
@author: essoca
"""

import sys, pygame
import numpy as np
from numpy.random import uniform as randm
pygame.init()

class Ball(object):
    
    def __init__(self, pos):
        self.x0, self.x = pos[0], pos[0]
        self.y0, self.y = pos[1], pos[1]
        self.v0x = 0
        self.v0y = 0
        self.radius = 10
        self.trajectory = []
        
    def launch(self, basket):
        """
            Determine the launch angle and initial speed
        """
        angle = np.arctan2(2*(height - basket[1])+basket[0], basket[0])
        speed = np.sqrt(0.5*g*(basket[0]**2+(2*(height-basket[1])+basket[0])**2)/(basket[0]+height-basket[1]))
        self.v0x = speed * np.cos(angle)
        self.v0y = speed * np.sin(angle)
        
    def move(self, t):
        """
            Trace the parabolic motion
        """
        self.x = self.v0x * t
        self.y = self.y0 - self.v0y * t + 0.5*g*(t**2)
        # Do not get out of the screen
        if self.y + self.radius > height:
            diff_height = self.y + self.radius - height
            self.y -= diff_height
        if self.x + self.radius > width:
            diff_width = self.x + self.radius - width
            self.x -= diff_width    
        self.trajectory.append((self.x, self.y))    
        
    def draw(self, screen, color):
        """
            Draw the basketball (circle)
        """
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        for n in range(len(self.trajectory)):
            xt = int(self.trajectory[n][0])
            yt = int(self.trajectory[n][1])
            pygame.draw.circle(screen, color, (xt, yt), 1, 1)
        
class Basket(object):

    def __init__(self, pos, diameter):
        self.x = pos[0]
        self.y = pos[1]
        self.diameter = diameter

    def draw(self, screen, color):         
        """
            Draw the basket (two small squares separated by diameter)
        """            
        sq_size = 8
        left_rect = (int(self.x - 0.5*self.diameter - 0.5*sq_size), int(self.y - 0.5*sq_size))
        right_rect = (int(self.x + 0.5*self.diameter - 0.5*sq_size), int(self.y - 0.5*sq_size))
        # Draw basket
        pygame.draw.rect(screen, color, (left_rect[0], left_rect[1], sq_size, sq_size))
        pygame.draw.rect(screen, color, (right_rect[0], right_rect[1], sq_size, sq_size))
        # Draw supports
        pygame.draw.line(screen, color, (right_rect[0] + sq_size, self.y),
                         (right_rect[0] + sq_size + self.diameter, self.y),2)
        pygame.draw.line(screen, color, (right_rect[0] + sq_size + self.diameter, self.y),
                         (right_rect[0] + sq_size + self.diameter, height),2)
        

white = (255,255,255)
blue = (0,0,255)  
red = (255,0,0)
g = 3.7

screen_size = width, height = 320*4, 240*4
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Playing basketball')  

# Create basket
basket_pos = randm()* width, randm()* height
basket = Basket(basket_pos, 20)
# Create and launch basketball
basketball = Ball((0,height))
basketball.launch(basket_pos)

t = 0
clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()            
                                                 
    dt = 0.01*clock.tick()
    screen.fill(white)                              
    basketball.draw(screen,blue)  
    basket.draw(screen,red)
    pygame.display.flip()
    t += dt               
    basketball.move(t)