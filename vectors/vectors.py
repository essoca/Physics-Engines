#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Randomly generate vectors and graphically add them by appropriate mouse dragging 
"""
import sys, pygame
import numpy as np
from numpy.random import uniform as randm
from numpy.random import randint
#import grading

pygame.init()


class Vector(object):
    
    def __init__(self,xy,thick_len=0.1,headSize_len=0.2,**kargs):
        "Convert to cartesian if polar coordinatesare given"
       
        if kargs["comp"] == "polar":
            self.x = xy[0] * np.cos(xy[1])
            self.y = -xy[0] * np.sin(xy[1])
        else:
            self.x = xy[0]
            self.y  = xy[1]
        self.thick_len = thick_len
        self.headSize_len = headSize_len 
    
    def get_headNtip(self,tail):
        """
            Get the coordinates of the head and tip of the vector
        """
        vec_length = np.sqrt(self.x**2 +self.y**2)
        vec_angle = np.arctan2(self.y,self.x)   
        
        head = [tail[0] + self.x, tail[1] + self.y]
        headSize = self.headSize_len * vec_length
        tip = [head[0] + headSize * np.cos(vec_angle), 
               head[1] + headSize * np.sin(vec_angle)]
        
        return head, tip

    def get_vertices(self,tail):
        """
            Get the coordinates of the vertices of the polygon defining the arrow
            representing the vector.
        """
        vec_length = np.sqrt(self.x**2 +self.y**2)
        vec_angle = np.arctan2(self.y,self.x)   
        sin_angle = np.sin(vec_angle)
        cos_angle = np.cos(vec_angle)
        
        head, tip = self.get_headNtip(tail)
        # Body
        half_thickness = 0.5 * self.thick_len * vec_length
        edge1_tail = [tail[0] + half_thickness * sin_angle,
                      tail[1] - half_thickness * cos_angle]
        edge2_tail = [tail[0] - half_thickness * sin_angle,
                      tail[1] + half_thickness * cos_angle]
        edge1_head = [head[0] + half_thickness * sin_angle,
                      head[1] - half_thickness * cos_angle]
        edge2_head = [head[0] - half_thickness * sin_angle,
                      head[1] + half_thickness * cos_angle]    
        # Head
        head_wing_size = 0.6 * 2 * half_thickness
        head_wing1 =  [edge1_head[0] + head_wing_size * sin_angle,
                       edge1_head[1] - head_wing_size * cos_angle]
        head_wing2 =  [edge2_head[0] - head_wing_size * sin_angle,
                       edge2_head[1] + head_wing_size * cos_angle]        
        
        vertices = [tail,edge1_tail,edge1_head,head_wing1,tip,head_wing2,
                    edge2_head,edge2_tail]         
        # Boundary conditions  
        # Find vertices of the polygon out of the screen        
        out_xr = [0] * len(vertices) 
        out_yd = [0] * len(vertices)
        out_xl = [0] * len(vertices) 
        out_yu = [0] * len(vertices)                
        for n, point in enumerate(vertices):
            if point[0] > screen_size[0]:
                out_xr[n] = point[0] - screen_size[0]
            if point[1] > screen_size[1]:    
                out_yd[n] = point[1] - screen_size[1]
            if point[0] < 0:
                out_xl[n] = -point[0]                
            if point[1] < 0:
                out_yu[n] = - point[1]                                
        max_out_xr = max(out_xr)        
        max_out_yd = max(out_yd)
        max_out_xl = max(out_xl)        
        max_out_yu = max(out_yu)        
        # Translate vector back in (if out)
        for n in range(len(vertices)):
            vertices[n][0] -= max_out_xr
            vertices[n][1] -= max_out_yd       
            vertices[n][0] += max_out_xl
            vertices[n][1] += max_out_yu  
                    
        return vertices            
    
    def draw(self,where,color,screen_size):
        """ 
            Draw the arrow representing the vector
        """
        vertices = self.get_vertices(where)                                            
        return pygame.draw.polygon(screen, color, vertices, 2)

def vector_clicked(vector,vec_rect,mouse_pos):
    """
        Return the label for the vector clicked on
    """
    clicked = False
    which = None
    for n in range(len(vec_rect)):        
        if vec_rect[n].collidepoint(mouse_pos):
            clicked, which = True, n
    return clicked, which        

def tail_on_head(tail1,tail2,vec2):
    """
        Check whether the tail of vec1 is on the head of vec2
    """
    head2, tip2 = vec2.get_headNtip(tail2)
    # Define triangular collision (with the head of vec2) as being within
    # the circle centered half way between the head and tip (half-way distance
    # being the radius).    
    vec2_angle = np.arctan2(vec2.y,vec2.x)
    rad = 0.5*np.sqrt((head2[0]-tip2[0])**2 + (head2[1]-tip2[1])**2)
    center = [head2[0] + rad*np.cos(vec2_angle),head2[1] + rad*np.sin(vec2_angle)]    
    if np.sqrt((tail1[0]-center[0])**2 + (tail1[1]-center[1])**2) <= rad:
        return True
    else:
        return False   
    
def add_vectors(list_vectors):
    """
        Add the vectors in the given list 
    """ 
    vec_sumx, vec_sumy = 0, 0
    for vec in list_vectors:
        vec_sumx, vec_sumy = vec_sumx + vec.x, vec_sumy + vec.y       
    return Vector([vec_sumx,vec_sumy],comp="cart")        

white = (255,255,255)
blue = (0,0,255)  
red = (255,0,0)

screen_size = width, height = 320*4, 240*4
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Adding vectors graphically')  
# Create and draw grading buttons
#project = grading.Grade(screen, width, height)

# Interval of allowed lengths for vectors
max_length = np.sqrt(width**2+height**2)
length_inf, length_sup = int(0.125*max_length), int(0.25*max_length)

num_vec = 2
vector, vec_tail, vec_rect = [], [], []
for n in range(num_vec):
    vector.append(Vector([randint(length_inf,length_sup),randm()*2*np.pi],comp="polar"))
    vec_tail.append([randm()*width,randm()*height])
    vec_rect.append(vector[n].draw(vec_tail[n],blue,screen_size))  
    
vec_sum = add_vectors(vector)
# Keep track of active heads and tails
active_head, active_tail = [1]*num_vec , [1]*num_vec   

vec_dragging = False
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:         
                inside_vec, m = vector_clicked(vector,vec_rect,event.pos)
                if inside_vec:
                    vec_dragging = True
                    mouse_x, mouse_y = event.pos    
                    offset_tail_x = vec_tail[m][0] - mouse_x
                    offset_tail_y = vec_tail[m][1] - mouse_y   
                # Check if project has been graded                                            
                #elif project.is_graded(event.pos): sys.exit()                                            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:    
                vec_dragging = False   
        elif event.type == pygame.MOUSEMOTION:
            if vec_dragging:
                mouse_x, mouse_y = event.pos
                vec_tail[m][0] = mouse_x + offset_tail_x
                vec_tail[m][1] = mouse_y + offset_tail_y  
                # Check if the tail of dragged vector is put on the head of
                # another vector (stick it if so)
                for n in range(num_vec):        
                    if tail_on_head(vec_tail[m],vec_tail[n],vector[n]):
                        vec_tail[m] = vector[n].get_headNtip(vec_tail[n])[0]                        
                        active_tail[m], active_head[n] = 0, 0    
                    elif tail_on_head(vec_tail[n],vec_tail[m],vector[m]):
                        vec_tail[n] = vector[m].get_headNtip(vec_tail[m])[0]                        
                        active_tail[n], active_head[m] = 0, 0                                     
                     
        screen.fill(white)
        # Draw grading buttons
        #project.draw_grading_buttons(screen)  
        for n in range(num_vec):
            vec_rect[n] = vector[n].draw(vec_tail[n],blue,screen_size)
        if active_tail.count(1) == 1 and active_head.count(1) == 1:
            # Draw the vector sum
            tail = vec_tail[np.where(active_tail)[0].tolist()[0]]          
            vec_sum.draw(tail,red,screen_size)
            vec_dragging = False
                
        pygame.display.flip()
        pygame.time.delay(1)
  