#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Break the knotted strings holding a block in equilibrium by changing the mass of the block 
@author: essoca
"""

import sys, pygame
import numpy as np
from numpy.random import uniform as randm
#import grading

pygame.init()


class KnottedString(object):
    
    def __init__(self, endup, endown):
        self.endup_x = endup[0]
        self.endup_y = endup[1]
        self.endown_x = endown[0]
        self.endown_y = endown[1]
        self.angle = np.arctan2(self.endown_y-self.endup_y,self.endown_x-self.endup_x)
        self.knot_x, self.knot_y = self.knot_string(randm())
        self.knot_where = np.sqrt((self.knot_x - self.endup_x)**2+(self.knot_y - self.endup_y)**2)
        self.endMidup_x, self.endMidup_y = self.knot_x, self.knot_y    
        self.knot_y0 =  self.knot_y 
        self.endown_y0 = self.endown_y          
        self.tension = 0
        self.max_tension = 375
        self.broken = False
         
    def knot_string(self, where):
        """
            Knot the string at a random position
        """
        # Check if left or right string
        slope = (self.endown_y-self.endup_y)/(self.endown_x-self.endup_x)
        knot_x = self.endup_x + (self.endown_x-self.endup_x) * where
        knot_y = self.endup_y + slope * (knot_x - self.endup_x)       
        return knot_x, knot_y    
    
    def is_broken(self):
        """
            If the tension exceeds the maximum tension, True. False otherwise
        """
        status = True if self.tension > self.max_tension else False
        return status
        
    def move_support(self, mouse_pos, mouse_offset, screen_size):
        """
            Update relevant string properties when the active end is dragged
        """
        # Move the active end
        self.endup_x = mouse_pos[0] + mouse_offset[0]
        self.endup_y = mouse_pos[1] + mouse_offset[1]
        # Active end can only move along the surface of the walls
        if self.endup_x > 0: 
            self.endup_y = 0
        else:
            self.endup_x = 0         
        # Active end can only move in upper-half plane  
        if self.endup_y < 0: self.endup_y = 0
        if self.endup_y > 0.5*screen_size[1]:
            self.endup_y = 0.5*screen_size[1]
        # Update angle (active end belong to a given quadrant in upper-half place) 
        tol, last_angle = 1e-8, self.angle
        self.angle = np.arctan2(self.endown_y-self.endup_y,self.endown_x-self.endup_x)        
        if last_angle <= 0.5*np.pi and self.angle > 0.5*np.pi:
            self.endup_x, self.angle = 0.5*screen_size[0] - tol, 0.5*np.pi - tol
        elif last_angle >= 0.5*np.pi and self.angle < 0.5*np.pi:
            self.endup_x, self.angle = 0.5*screen_size[0] + tol, 0.5*np.pi + tol    
        # Update knot position    
        self.knot_x = self.endup_x + self.knot_where * np.cos(self.angle)
        self.knot_y = self.endup_y + self.knot_where * np.sin(self.angle)
   
    def fall(self, t, screen_height, block_height):
        """
            Move the broken part of the string (if any) that is in contact with block
        """
        if self.broken:
            self.knot_y = self.knot_y0 + 0.5*g*t**2
            self.endown_y = self.endown_y0 + 0.5*g*t**2
            if self.endown_y > screen_height - block_height:
                diff_height = self.endown_y - screen_height + block_height
                self.endown_y -= diff_height
                self.knot_y -= diff_height
        
    def draw(self,screen,color):
        """
            Draw the knotted string
        """
        knot_radius = 5
        if not self.broken:
            # String
            pygame.draw.line(screen, color, (self.endup_x,self.endup_y), 
                             (self.endown_x,self.endown_y),2)
            # Knot
            pygame.draw.circle(screen, color, (int(self.knot_x),int(self.knot_y)), knot_radius)                    
        else:
            # String attached to support
            pygame.draw.line(screen, color, (self.endup_x,self.endup_y), 
                             (self.endMidup_x,self.endMidup_y),2)
            # String falling
            pygame.draw.line(screen, color, (self.knot_x,self.knot_y), 
                             (self.endown_x,self.endown_y),2)
            # Knot
            pygame.draw.circle(screen, color, (int(self.knot_x),int(self.knot_y)), knot_radius)            
        
class HangingBlock(object):

    def __init__(self,size,pos,mass=30):        
        self.x = pos[0]
        self.y = pos[1]
        self.y0 = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.mass = mass
        
    def move(self, t, screen_height):
        """
            Change the coordinates of the block according to a free fall
        """
        self.y = self.y0 + 0.5*g*t**2
        # Do not get out of the screen
        if self.y + 0.5*self.height > screen_height:
            diff_height = self.y + 0.5*self.height - screen_height
            self.y -= diff_height
            #sys.exit()
        
    def draw(self,screen,color):
        """
            Draw a rectangular block
        """
        left, top = self.x - 0.5*self.width, self.y - 0.5*self.height
        pygame.draw.rect(screen,color,(left,top,self.width,self.height),2)

def is_string_end_dragged(strings, mouse_pos):
    """
        True if the active end of a string is clicked, False otherwise
        Return which string
    """
    clicked = False
    which = None
    for n in range(len(strings)):        
        if np.sqrt((strings[n].endup_x-mouse_pos[0])**2 + 
                   (strings[n].endup_y-mouse_pos[1])**2) < 50:
            clicked, which = True, n
    return clicked, which 

def apply_tension(strings, hanging_weight):
    """
        Apply tension in the strings according to the hanging weight and 
        the angles subtended by each string
    """
    angle_l = strings[0].angle
    angle_r = np.pi - strings[1].angle                     
    sin_sum_angles = np.sin(angle_l + angle_r) 
    strings[0].tension = abs(np.cos(angle_r) * hanging_weight / sin_sum_angles)
    strings[1].tension = abs(np.cos(angle_l) * hanging_weight / sin_sum_angles) 
    if strings[0].is_broken():
        strings[0].broken = True
    if strings[1].is_broken():
        strings[1].broken = True
                

white = (255,255,255)
blue = (0,0,255)  
red = (255,0,0)

screen_size = width, height = 320*4, 240*4
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Breaking the knotted strings')  

# Ends of the strings
l_up = l_up_x, l_up_y = 0.5*randm()*width, 0
r_up = r_up_x, r_up_y = (1-0.5*randm())*width, 0
l_down = l_down_x, l_down_y = 0.5*width, 0.5*height
r_down = r_down_x, r_down_y = 0.5*width, 0.5*height  
# Build strings
string = [KnottedString(l_up,l_down), KnottedString(r_up,r_down)]
# Block dimensions and position of its center
block_width, block_height = 100, 100
pos_x, pos_y = l_down_x, l_down_y + 0.5*block_height
block = HangingBlock((block_width, block_height),(pos_x, pos_y))
block_weight = float(sys.argv[1])
# Apply tension to strings
apply_tension(string, block_weight)

dragging_string_end = False
# gravitational acceleration
g = 3.7
t = 0
clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:    
                dragging_string_end, which = is_string_end_dragged(string,event.pos)
                if dragging_string_end:
                    offset_x = string[which].endup_x - event.pos[0]
                    offset_y = string[which].endup_y - event.pos[1]
                    mouse_offset = offset_x, offset_y                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                dragging_string_end = False 
        elif event.type == pygame.MOUSEMOTION:
            if dragging_string_end: 
                string[which].move_support(event.pos,mouse_offset,screen_size)
                apply_tension(string, block_weight)                  
                if string[0].broken or string[1].broken:
                    dragging_string_end = False
         
    if string[0].broken or string[1].broken:
        dt = clock.tick()/100
        t += dt 
        string[0].fall(t,height,block.height)
        string[1].fall(t,height,block.height)
        block.move(t,height)                       
    screen.fill(white)                              
    string[0].draw(screen,blue)
    string[1].draw(screen,blue)                               
    block.draw(screen,red)        
    pygame.display.flip() 
    
## Project not finished yet    
                      
