"""
Play basketball with bouncing (and drag): 
Euler method for motion, so there is error.
@author: essoca
"""

import sys, pygame
import numpy as np
from numpy.random import uniform as randm
pygame.init()

class Ball(object):
    
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]        
        self.vx = 0
        self.vy = 0
        self.cor = 0.1
        self.radius = 10
        self.trajectory = []
        
    def launch(self, basket):
        """
            Determine the launch angle and initial speed
        """
        angle = np.arctan2(2*(height - basket[1])+basket[0], basket[0])
        speed = np.sqrt(0.5*g*(basket[0]**2+(2*(height-basket[1])+basket[0])**2)/(basket[0]+height-basket[1]))
        self.vx = speed * np.cos(angle)
        self.vy = speed * np.sin(angle)        
        
    def move(self, dt, basket):
        """
            Trace the parabolic motion
        """
        
        def apply_bc(x, y, vx, vy, basket):
            ball_edge_horz_l = x - self.radius
            ball_edge_horz_r = x + self.radius
            ball_edge_vert_d = y + self.radius
            # Do not get out of the screen
            if ball_edge_vert_d > height and ball_edge_horz_l > 2*self.radius:                
                diff_height = ball_edge_vert_d - height
                y -= diff_height
                vy = -(1-self.cor) * vy
            if ball_edge_horz_r > width:
                diff_width = ball_edge_horz_r - width
                x -= diff_width  
                vx = -(1-self.cor) * vx
            if ball_edge_horz_l < 0 and ball_edge_vert_d < height - 2*self.radius:                
                x -= ball_edge_horz_l               
                vx = -(1-self.cor) * vx    
            # Bounce from basket          
            if basket.basket_vert_u[0] - x <= self.radius:
               x -=  self.radius - (basket.basket_vert_u[0] - x)
               vx = -(1-self.cor) * vx                
                
            return (x, y, vx, vy)       
        # Update position
        self.x += self.vx *dt
        self.y -= self.vy *dt
        # Update velocity
        self.vx += -gamma * self.vx *dt
        self.vy -= (g + gamma * self.vy) *dt
        # Apply boundary conditions                           
        self.x, self.y, self.vx, self.vy = apply_bc(self.x, self.y, self.vx, self.vy, basket) 
        self.trajectory.append((self.x, self.y))  
        
                           
    def draw(self, screen, color):
        """
            Draw the basketball (circle)
        """
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        # Draw trajectory in presence of drag
        for n in range(len(self.trajectory)):
            xdt = int(self.trajectory[n][0])
            ydt = int(self.trajectory[n][1])
            pygame.draw.circle(screen, color, (xdt, ydt), 1, 1)    
        
class Basket(object):

    def __init__(self, pos, diameter):
        self.x = pos[0]
        self.y = pos[1]
        sq_size = 8
        left_rect = (int(self.x - 0.5*diameter - 0.5*sq_size), int(self.y - 0.5*sq_size))
        right_rect = (int(self.x + 0.5*diameter - 0.5*sq_size), int(self.y - 0.5*sq_size))
        self.basket_left = (left_rect[0], left_rect[1], sq_size, sq_size)
        self.basket_right = (right_rect[0], right_rect[1], sq_size, sq_size)
        # Horizontal support
        self.basket_horz_l = (right_rect[0] + sq_size, self.y)
        self.basket_horz_r = (right_rect[0] + sq_size + diameter, self.y)
        # Vertical support
        self.basket_vert_u = (right_rect[0] + sq_size + diameter, self.y)
        self.basket_vert_d = (right_rect[0] + sq_size + diameter, height)

    def draw(self, screen, color):         
        """
            Draw the basket (two small squares separated by diameter)
        """            
        # Draw basket
        pygame.draw.rect(screen, color, self.basket_left)
        pygame.draw.rect(screen, color, self.basket_right)
        # Draw supports
        pygame.draw.line(screen, color, self.basket_horz_l, self.basket_horz_r,2)
        pygame.draw.line(screen, color, self.basket_vert_u, self.basket_vert_d,2)
        

white = (255,255,255)
blue = (0,0,255)  
red = (255,0,0)
g = 3.7
gamma = 0

screen_size = width, height = 320*4, 240*4
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Playing basketball drag & bounce')  

# Create basket
basket_pos = randm()* width, randm()* height
basket = Basket(basket_pos, 20)
# Create and launch basketball
basketball = Ball((0,height))
basketball.launch(basket_pos)

clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()            
                                                 
    dt = 0.01*clock.tick()
    screen.fill(white)                              
    basketball.draw(screen, blue)  
    basket.draw(screen,red)
    pygame.display.flip()               
    basketball.move(dt, basket)
