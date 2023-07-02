#solar system
import pygame
import numpy as np
import os

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

Center = ( WINDOW_WIDTH/2. , WINDOW_HEIGHT/2. )

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
ufo_image = pygame.image.load(os.path.join(assets_path, 'ufo.png'))

pygame.init()
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
clock = pygame.time.Clock()

# functions ===============================================================
def getRegularPolygon(nvertices, radius):  # get coordinates of polygon centered at the origin
    rad = 2*np.pi/nvertices
    v = np.zeros( (nvertices, 2), dtype=np.float32)
    for i in range(nvertices):
        x = radius * np.cos(rad * i)
        y = radius * np.sin(rad * i)
        v[i,0] = x
        v[i,1] = y
    return v

def getRandomColor():
    return (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))


def Rmat(deg):
    rad = np.deg2rad(deg)
    v = np.array([ [np.cos(rad), -np.sin(rad), 0]
                  ,[np.sin(rad),  np.cos(rad), 0]
                  ,[0          ,  0          , 1] ])
    return v

def Tmat(a ,b):
    v = np.array([ [1, 0, a]
                  ,[0, 1, b]
                  ,[0, 0, 1] ])
    return v




# classes =================================================================
class body():
    def __init__(self, nvertices, radius, center = Center, color = (200,200,200), dist = 0):
        self.p = getRegularPolygon(nvertices, radius)
        angle = np.deg2rad(np.random.randint(0,360))

        self.center = np.array(center) + np.array([np.cos(angle), np.sin(angle)]) * dist #start from a random position
        self.color = color
        self.p = self.p + self.center 
        self.dist = dist

    def update(self, matrix):
        R = matrix[0:2, 0:2]
        t = matrix[0:2, 2]
        self.p = ( R @ self.p.T ).T + t
        self.center = ( R @ self.center.T).T + t

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.p)
        

class planet():
    def __init__(self, you, revolution, rotation, centerbody):
        self.you = you         # "body" class
        self.rev = revolution
        self.rot = rotation
        self.axis = centerbody # "body" class

    def update(self,):
        matErev = Tmat(self.axis.center[0], self.axis.center[1]) @ Rmat(self.rev) @ Tmat(-self.axis.center[0], -self.axis.center[1])
        matErot = Tmat(self.you.center[0], self.you.center[1]) @ Rmat(self.rot) @ Tmat(-self.you.center[0], -self.you.center[1])
        matE = matErev @ matErot

        self.you.update(matE)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.you.color, self.you.p)
        
    

# main function ============================================================
def main():
    planets = []
    angleS = 1
    angleErev = .01
    angleErot = 1
    angleMrev = 0.1
    angleMrot = 0.1

    distSE = 300
    distEM = 120

    Sun = body(20, 50, Center, (255,0,0))
    Earth = body(5, 20, Sun.center, (0,0,255), distSE)
    Moon = body(4, 10, Earth.center, (239, 245, 66), distEM)

    planets.append(planet(Earth, angleErev, angleErot, Sun))
    planets.append(planet(Moon, angleMrev, angleMrot, Earth))

    Earth2 = body(10, 27, Sun.center, getRandomColor(), 370)
    planets.append(planet(Earth2, 0.02, 0.7, Sun))

    Moon1 = body(13, 7, Earth2.center, getRandomColor(), 70)
    Moon2 = body(9, 7, Earth2.center, getRandomColor(), 120)

    MoonMoon = body(3, 5, Moon1.center, getRandomColor(), 35)

    planets.append(planet(Moon1, 0.13, 0.24, Earth2))
    planets.append(planet(Moon2, 0.72, 0.2, Earth2))
    planets.append(planet(MoonMoon, 0.1, 0.1, Moon1))

        # ufo position and velocity
    ufo_x = np.array([np.random.randint(WINDOW_WIDTH), np.random.randint(WINDOW_HEIGHT)], dtype='float')
    ufo_v = np.zeros((2,), dtype='float')
    ufo_a = np.zeros((2,), dtype='float')

    done = False
    while not done:
        #1 event check ======================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        #2 logic =============================================================
        matS = Tmat(Sun.center[0], Sun.center[1]) @ Rmat(angleS) @ Tmat(-Sun.center[0], -Sun.center[1])
        Sun.update(matS)
        
        for p in planets:
            p.update()

        ufo_a = np.array([np.random.uniform(-1,1),np.random.uniform(-1,1)])
        ufo_v += ufo_a
        ufo_x += ufo_v

        if ufo_x[0] < - WINDOW_WIDTH / 2.:
            ufo_v[0] *= -1.
            ufo_x[0] = - WINDOW_WIDTH / 3.

        if ufo_x[0] > 3 * WINDOW_WIDTH / 2.:
            ufo_v[0] *= -1.
            ufo_x[0] = 4 * WINDOW_WIDTH / 3.
        
        if ufo_x[1] < - WINDOW_HEIGHT / 2.:
            ufo_v[1] *= -1.
            ufo_x[1] = - WINDOW_HEIGHT / 3.

        if ufo_x[1] > 3 * WINDOW_HEIGHT / 2.:
            ufo_v[1] *= -1.
            ufo_x[1] = 4 * WINDOW_HEIGHT / 3.


        #3 draw ==============================================================
        screen.fill((0,0,10))
        Sun.draw(screen)
        
        for p in planets:
            p.draw(screen)

            #draw ufo
        screen.blit(ufo_image, ufo_x)



        pygame.display.flip()
        clock.tick(60)
    pass

if __name__ == "__main__" :
    main()



###########
#image source from : <a href="https://www.flaticon.com/free-icons/ufo" title="ufo icons">Ufo icons created by Freepik - Flaticon</a>
###########
