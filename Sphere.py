import pygame
import math
import numpy as np
import random


pygame.init()

screen = pygame.display.set_mode((400,400))
screen.fill((0,0,0))
pygame.display.set_caption("Electrostatics")
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 10, bold=True)  

normalpt = font.render('o', True,
            pygame.Color(100, 100, 100, 225),
            pygame.Color(0, 0, 0, 0))

mainpt = font.render('@', True,
            pygame.Color(255, 225, 255, 225),
            pygame.Color(0, 0, 0, 0))



def GetPtOnSp(r,t,p):
    x = r*np.sin(p)*np.cos(t)
    y = r*np.cos(p)
    z = r*np.sin(p)*np.sin(t)
    return (x,y,z)

def GeneratePoints(R):
    density = 0.1
    #number of points = density x length
    pnum = np.linspace(0, 2*np.pi, math.ceil(density*2*np.pi*R))
    points = []
    for p in pnum:
        r = abs(R*np.sin(p))
        tnum = np.linspace(0, 2*np.pi, math.ceil(density*2*np.pi*r))
        for t in  tnum:
            points.append(GetPtOnSp(R,t,p))
    return points

def TransformPoints(points):
    tpoints = []
    focal_dist = 600
    for point in points:
        if point[2] != 0:
            xt = point[0]*focal_dist/(point[2] - 200) 
            yt = point[1]*focal_dist/(point[2] - 200)
        else:
            xt = point[0] 
            yt = point[1] 
        tpoints.append((xt, yt))
    return tpoints

def RotateX(points, angle):
    if angle == 0:
        return points
    rpoints = []
    for point in points:
        x = point[0]
        y = point[1]*math.cos(angle) - point[2]*math.sin(angle)
        z = point[1]*math.sin(angle) + point[2]*math.cos(angle)
        rpoints.append((x,y,z))
    return rpoints


def RotateY(points, angle):
    if angle == 0:
        return points
    rpoints = []
    for point in points:
        x = point[0]*math.cos(angle) + point[2]*math.sin(angle)
        y = point[1]
        z = -point[0]*math.sin(angle) + point[2]*math.cos(angle)
        rpoints.append((x,y,z))
    return rpoints


def GetXY(r, p, t):
    cor = GetPtOnSp(50, np.pi/2, np.pi/4)
    rcor = RotateY([RotateX([cor], ax)[0]], ay)[0]
    tcor = TransformPoints([rcor])[0]
    return tcor




plotpoints = GeneratePoints(50)
ax = 0.8
ay = np.pi/3



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.KEYDOWN == pygame.K_ESCAPE:
            pygame.quit()
            running = False

    rpoints = RotateX(plotpoints, ax)
    rpoints = RotateY(rpoints, ay)
    tpoints = TransformPoints(rpoints)

    # Clear Screen to remove old points
    screen.fill((0,0,0))

    for point in tpoints:
        screen.blit(normalpt, (point[0] + screen.get_size()[0]/2, point[1] + screen.get_size()[1]/2))
         

    
    ax += 0.01
    ay += 0.015
    if ax >= 2*np.pi:
        ax = 0
    if ay >= 2*np.pi:
        ay = 0

    clock.tick(60)

    pygame.display.update()



#print(type(np.linspace(0, np.pi, 10)))