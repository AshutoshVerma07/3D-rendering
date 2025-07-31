import numpy as np
import math
import pygame
import matplotlib.pyplot as plt

pygame.init()

scr = pygame.display.set_mode((600,600))
pygame.display.set_caption("Donut")
scr.fill((0,0,0))
clock = pygame.time.Clock()


ax = 0
ay = 0
wx = 0.01
wy = 0.01

running = True
font = pygame.font.SysFont('Arial', 10, bold=True)   
img = font.render('0', True,
            pygame.Color(225, 225, 225, 225),
            pygame.Color(0, 0, 0, 0))



# return a list of points on the surface of donut given it's innner and outer radius
def GetPointsonCube(len):
    len /= 2
    density = 8
    xs = np.linspace(-len, len, density)
    points = []
    for a in xs:
        for b in xs:
            points.append((a,b,len))
            points.append((a,b,-len))
            points.append((a,len,b))
            points.append((a,-len,b))
            points.append((len,a,b))
            points.append((-len,a,b))
    return points
    

# takes in list of points and return the x and y coordinate by projecting 3D into 2D considering perspective
def Transformto2D(points, focal_dist):
    tpoints = []
    for point in points:
        if point[2] != 0:
            xt = point[0]*focal_dist/(point[2] + 20) 
            yt = point[1]*focal_dist/(point[2] + 20)
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





# generate 3D points
points = GetPointsonCube(len=10)
# transform those points to fit 2D perspective
#tpoints = Transformto2D(points, focal_dist=100)
print(RotateX(points, np.pi))


while running:
    # check for quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    char = font.render("O", True,
                pygame.Color(225, 225, 225, 225),
                pygame.Color(0, 0, 0, 0))
    
    # rotate point about x and y axis
    rpoints = RotateY(RotateX(points, ax), ay)
    # transform those rotated points into 2D coordinates
    rtpoints = Transformto2D(rpoints, focal_dist=250)
    # remove old points by filling the screen with black color
    scr.fill((0,0,0))
    #render each point in the list of points
    for point in rtpoints:
        scr.blit(char, (point[0] + scr.get_size()[0]/2, point[1] + scr.get_size()[1]/2))

    if ax >= 2*np.pi:
        ax = 0
    ax += wx

    if ay >= 2*np.pi:
        ay = 0
    ay += wy
    
    
    scr.blit(char, (0, 0))
    clock.tick(60)

    pygame.display.update()






'''x=[]
y=[]
for tp in tpoints:
    x.append(tp[0])
    y.append(tp[1])

print(x)

plt.scatter(x, y, color='blue', marker='o')  # 'o' = circle marker
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('2D Scatter Plot')
plt.grid(True)
plt.axis('equal')  # Optional: make aspect ratio 1:1
plt.show()'''