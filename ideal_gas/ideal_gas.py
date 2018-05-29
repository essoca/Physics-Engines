#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ideal gas
@author: essoca
"""

import sys, pygame
import numpy as np
from numpy.random import uniform as randm
from numpy.random import normal as rnorm
from numpy.random import rayleigh as chidf2
import matplotlib.pyplot as plt

pygame.init()

class Container(object):

    def __init__(self, pos_top):
        # intantaneous position of movable piston
        self.y = pos_top
        # height when not moving the piston (history recorded)
        self.heq = []
        # pressure of container when not moving piston (history recorded)
        self.peq = []
        self.measure_peq = False
        # State of piston
        self.moving_piston = False
        # vectors capturing the change of momentum (perp to wall surface)
        # of particles colliding with walls. An entry for each particle
        # that collides
        self.top = []
        self.bottom = []
        self.left = []
        self.right = []
   
    def compute_pressure(self):
        """
            Compute average pressure
        """
        # Average impulses on walls 
        It, Ib = np.mean(self.top), np.mean(self.bottom)
        Il, Ir = np.mean(self.left), np.mean(self.right)
        Iavg = np.mean([It, Ib, Il, Ir])
        # Average frequency of arrival
        ft, fb = len(self.top), len(self.bottom) 
        fl, fr = len(self.left), len(self.right)
        favg = np.mean([ft, fb, fl, fr])
        # Average pressure
        self.peq.append(Iavg * favg)        
        self.top = []
        self.bottom = []
        self.left = []
        self.right = []
     
    def draw(self, screen):
        """
            Draw a line delimiting the top of the container
        """    
        pygame.draw.line(screen, black, (0, self.y), (width, self.y), 2)
    
    
class Particle(object):
    
    def __init__(self, pos, vel, color, radius, filled):
        self.x = pos[0]
        self.y = pos[1]        
        self.v = vel[0]
        self.angle = vel[1]
        self.radius = radius
        self.color = color
        self.filled = filled 
        
    def move(self, dt, container):
        """
            Move at constant speed
        """        
        def apply_bc(x, y, v, angle):
            ball_edge_horz_l = x - self.radius
            ball_edge_horz_r = x + self.radius
            ball_edge_vert_u = y - self.radius
            ball_edge_vert_d = y + self.radius
            # Do not get out of the screen
            impulse_y = abs(2* v* np.sin(angle))
            impulse_x = abs(2* v* np.cos(angle))
            if ball_edge_vert_u < container.y:                
                y -= ball_edge_vert_u - container.y
                angle = -angle
                if container.measure_peq: 
                    container.top.append(impulse_y)
            if ball_edge_vert_d > height:                
                y -= (ball_edge_vert_d - height)
                angle = -angle
                if container.measure_peq:
                    container.bottom.append(impulse_y)
            if ball_edge_horz_r > width:
                x -= (ball_edge_horz_r - width) 
                angle = np.pi - angle
                if container.measure_peq:
                    container.right.append(impulse_x)
            if ball_edge_horz_l < 0:                
                x -= ball_edge_horz_l               
                angle = np.pi - angle                                 
                if container.measure_peq:                    
                    container.left.append(impulse_x)
            return (x, y, angle)       
        # Update position
        self.x += self.v * np.cos(self.angle) * dt
        self.y += self.v * np.sin(self.angle) * dt
        # Apply boundary conditions                           
        self.x, self.y, self.angle = apply_bc(self.x, self.y, self.v, self.angle) 
        
        return container
                           
    def draw(self, screen):
        """
            Draw the particle (circle)
        """
        fill = 0 if self.filled else 2
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, fill)
        
        
def initialize_gas(container):
    """
        Initial configuration of particles in the gas
    """        
    lx = width - radius
    ly = height - radius
    gas = []
    np.random.seed(1)
    for n in range(N):
        rx, ry = randm(), randm()
        x = rx * radius + (1-rx)*lx 
        y = ry * (container.y + radius) + (1-ry)*ly    
        #v = rnorm((2/np.sqrt(np.pi))*np.sqrt(T), np.sqrt(T))                     
        v = chidf2(np.sqrt(kT_m))
        angle = 2* np.pi* randm()
        gas.append(Particle((x,y), (v, angle), black, radius, True))    
    return gas           

def is_piston_dragged(container, mouse_posy):
    """
        Boolean indicating if there is mouse collision with piston
    """
    if abs(container.y - mouse_posy) < 20:
        return True
    else:
        return False

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)  
red = (255,0,0)

screen_size = width, height = 320*4, 240*4
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Ideal gas')  


# Create balls
N = 100
kT_m = 1e5
m = 5

radius = 20
piston_pos = 50
container = Container(piston_pos)
particles = initialize_gas(container)


clock = pygame.time.Clock()
elapsed_time = 0 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            l = np.arange(height - piston_pos, container.heq[-1], -1)
            p = m* N * kT_m/ l
            plt.plot(container.heq, container.peq,'ro',l,p)
            plt.xlabel("Height")
            plt.ylabel("Pressure")
            plt.gca().legend(("measured", "expected"))
            plt.savefig('testplot.png')
            sys.exit()        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if is_piston_dragged(container, event.pos[1]):
                    container.moving_piston = True 
                    container.measure_peq = False
                    mouse_offset = container.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                container.moving_piston = False  
                container.measure_peq = True
                container.heq.append(height - container.y)       
                elapsed_time = 0                                            
        elif event.type == pygame.MOUSEMOTION:
            if container.moving_piston:
                # Movable piston (top of container)
                container.y = event.pos[1] + mouse_offset                    
    dt = 0.01*clock.tick()
    # Time in units of dt
    elapsed_time += 1
    screen.fill(white) 
    # Draw the gas of particles
    for n in range(len(particles)):                             
        particles[n].draw(screen)
    # Draw the container of this gas
    container.draw(screen)    
    pygame.display.flip()   
    for n in range(len(particles)):                   
        container = particles[n].move(dt, container)
    if container.measure_peq and elapsed_time == 110:    
        container.compute_pressure()
    #print(container.yeq,container.peq)    