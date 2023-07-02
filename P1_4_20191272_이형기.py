import pygame
import numpy as np

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

Center = np.array([ 3 * WINDOW_WIDTH/4. , WINDOW_HEIGHT/2.])
Center2 = np.array([ WINDOW_WIDTH/4. , WINDOW_HEIGHT/2.])

pygame.init()
screen = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT) )
clock = pygame.time.Clock()

# functions ======================================================
def Tmat(a, b):
    v = np.array([[1, 0, a]
                 ,[0, 1, b]
                 ,[0, 0, 1]])
    return v

def Rmat(th):
    rad = np.deg2rad(th)
    v = np.array([[np.cos(rad), -np.sin(rad), 0]
                 ,[np.sin(rad),  np.cos(rad), 0]
                 ,[0         ,           0, 1]])
    return v

def Checkwin(beetle1, beetle2):
    diff121 = beetle1.p[2] - beetle2.center
    dist121 = np.sqrt(diff121[0]**2 + diff121[1]**2)
    diff122 = beetle1.p[4] - beetle2.center
    dist122 = np.sqrt(diff122[0]**2 + diff122[1]**2)

    diff211 = beetle2.p[2] - beetle1.center
    dist211 = np.sqrt(diff211[0]**2 + diff211[1]**2)
    diff212 = beetle2.p[4] - beetle1.center
    dist212 = np.sqrt(diff212[0]**2 + diff212[1]**2)

    dist12 = np.min([dist121, dist122])
    dist21 = np.min([dist211, dist212])



    if dist12 < beetle2.size :
        return 1
    
    elif dist21 < beetle1.size :
        return 2

    else :
        return 0

# classes ========================================================
class Beetle():
    def __init__(self, size, startingposition, startingangle, color = (50, 168, 82)):
        self.p = size * np.array([[1,1], [-1,1], [-1,-2], [0,-1], [1,-2]])
        self.p =  self.p + startingposition
        #self.horn = np.array([self.p[2], self.p[4]])
        self.color = color
        self.dv = 0
        self.dth = 0
        self.center = startingposition
        self.angle = startingangle
        self.size = size
        M = Tmat(self.center[0], self.center[1]) @ Rmat(self.angle) @ Tmat(-self.center[0], -self.center[1])

        R = M[0:2, 0:2]
        t = M[0:2, 2]
        self.p = ( R @ self.p.T).T + t

    
    def update1(self,):
        rad = np.deg2rad(self.angle - 90)
        self.p += self.dv * np.array([np.cos(rad), np.sin(rad)])
        self.center += self.dv * np.array([np.cos(rad), np.sin(rad)])

    def update2(self,):
        self.angle += self.dth
        M = Tmat(self.center[0], self.center[1]) @ Rmat(self.dth) @ Tmat(-self.center[0], -self.center[1])

        R = M[0:2, 0:2]
        t = M[0:2, 2]
        self.p = ( R @ self.p.T).T + t

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.p)


# main ===========================================================
def main():

    beetle1 = Beetle(10, Center, np.random.randint(360), (0,0,0))
    beetle2 = Beetle(10, Center2, np.random.randint(360))


    done = False
    while not done:
        # 1 event check ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

                elif event.key == pygame.K_DOWN:
                    beetle1.dv = -3
                elif event.key == pygame.K_UP:
                    beetle1.dv = 3
                elif event.key == pygame.K_RIGHT:
                    beetle1.dth = 3
                elif event.key == pygame.K_LEFT:
                    beetle1.dth = -3

                elif event.key == pygame.K_s:
                    beetle2.dv = -3
                elif event.key == pygame.K_w:
                    beetle2.dv = 3
                elif event.key == pygame.K_d:
                    beetle2.dth = 3
                elif event.key == pygame.K_a:
                    beetle2.dth = -3
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    beetle1.dv = 0
                elif event.key == pygame.K_UP:
                    beetle1.dv = 0
                elif event.key == pygame.K_RIGHT:
                    beetle1.dth = 0
                elif event.key == pygame.K_LEFT:
                    beetle1.dth = 0

                if event.key == pygame.K_s:
                    beetle2.dv = 0
                elif event.key == pygame.K_w:
                    beetle2.dv = 0
                elif event.key == pygame.K_d:
                    beetle2.dth = 0
                elif event.key == pygame.K_a:
                    beetle2.dth = 0

        

        # 2 logic ================================================
        beetle1.update1()
        beetle1.update2()

        beetle2.update1()
        beetle2.update2()

        Check = Checkwin(beetle1, beetle2)
        if Check == 1:
            print("beetle1 wins")
            done = True

        elif Check == 2:
            print("beetle2 wins")
            done = True




        # 3 draw ==================================================
        screen.fill((230,230,230))
        beetle1.draw(screen)
        beetle2.draw(screen)




        # 4
        pygame.display.flip()
        clock.tick(60)
    pass

if __name__ == "__main__":
    main()

