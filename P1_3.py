#rotating arms

import pygame
import numpy as np

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000
First_Joint = (300,300)

pygame.init()
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
clock = pygame.time.Clock()

#Functions ======================================================
def getArm(width, height, x=0, y=0):
    v = np.array([ [x, y], [x+width, y], [x+width, y+height], [x, y+height] ])

    return v

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


#Classes ========================================================
class Arm():
    def __init__(self, width, height, fixedP = First_Joint):
        self.width = width
        self.height = height
        self.p = getArm(width, height)
        self.pt = self.p.T
        self.angle = 45.
        self.position = fixedP
        self.angle_dx = 0

    def update(self,):
        self.angle += self.angle_dx
        M = Tmat(self.position[0], self.position[1]) @ Rmat(self.angle) @ Tmat( -(self.height)/2, -(self.height)/2)

        R2x2 = M[0:2, 0:2]
        tvec = M[0:2, 2]
        self.Q = (R2x2 @ self.pt).T + tvec

    def draw(self, screen):
        pygame.draw.polygon(screen, (100,200,250), self.Q, width = 3)

class Arm2(Arm):
    def __init__(self, width, height, fixedP):
        super().__init__(width, height, fixedP)
    
    def update(self, previous_position):
        self.angle += self.angle_dx
        self.position = previous_position
        M = Tmat(self.position[0], self.position[1]) @ Rmat(self.angle) @ Tmat( -(self.height)/2, -(self.height)/2)

        R2x2 = M[0:2, 0:2]
        tvec = M[0:2, 2]
        self.Q = (R2x2 @ self.pt).T + tvec

class Grip():
    def __init__(self, width, height, startingP):
        self.width = width
        self.height = height
        self.grip = getArm(width, height, startingP[0], startingP[1]) + [-self.height/2. , -self.height/2.]
        self.angle = 45.

        M = Tmat(startingP[0], startingP[1]) @ Rmat(90) @ Tmat(-startingP[0] , -startingP[1])

        self.grip1 = self.grip

        R = M[0:2, 0:2]
        t = M[0:2, 2]
        self.grip2 = ( R @ self.grip.T).T + t

        self.angle_dx = 0
        

    def update1(self, armposition):
        self.angle += self.angle_dx
        M = Tmat(armposition[0], armposition[1]) @ Rmat(self.angle_dx) @ Tmat(-armposition[0] , -armposition[1])
        
        R = M[0:2, 0:2]
        t = M[0:2, 2]
        self.grip1 = ( R @ self.grip1.T).T + t
        self.grip2 = ( R @ self.grip2.T).T + t

    def update2(self, arm):
        L = arm.width - arm.height
        position_1 = arm.position + L * np.array([np.cos(arm.angle), np.sin(arm.angle)])
        
        M = Tmat(arm.position[0], arm.position[1]) @ Rmat(arm.angle_dx) @ Tmat(-arm.position[0] , -arm.position[1])

        R = M[0:2, 0:2]
        t = M[0:2, 2]

        position_2 = ( R @ position_1.T).T + t

        diff = position_2 - position_1

        self.grip1 = self.grip1 + diff
        self.grip2 = self.grip2 + diff
        
    def draw(self, screen):
        pygame.draw.polygon(screen, (100,200,250), self.grip1)
        pygame.draw.polygon(screen, (100,200,250), self.grip2)


        
#main ==========================================================

def main():
    
    arm1 = Arm(200., 30., First_Joint)
    
    L1 = arm1.width - arm1.height
    Second_Joint = (arm1.position[0] + L1 * np.cos(np.deg2rad(arm1.angle)), arm1.position[1] + L1 * np.sin(np.deg2rad(arm1.angle)))
    arm2 = Arm2(300., 25., Second_Joint)

    L2 = arm2.width - arm2.height
    Third_Joint = (arm2.position[0] + L2 * np.cos(np.deg2rad(arm2.angle)), arm2.position[1] + L2 * np.sin(np.deg2rad(arm2.angle)))
    arm3 = Arm2(300., 20., Third_Joint)

    L3 = arm3.width - arm3.height
    Last_Joint = (arm3.position[0] + L3 * np.cos(np.deg2rad(arm3.angle)), arm3.position[1] + L3 * np.sin(np.deg2rad(arm3.angle)))
    

    grip = Grip(100, 18, Last_Joint)

    done = False
    press = 0
    while not done:
        #1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            
                elif event.key == pygame.K_q:
                    arm1.angle_dx -= 3.
                    grip.angle_dx -= 3.
                    press = 1
                elif event.key == pygame.K_w:
                    arm1.angle_dx += 3.
                    grip.angle_dx += 3.
                    press = 1

                elif event.key == pygame.K_a:
                    arm2.angle_dx -= 3.
                    grip.angle_dx -= 3.
                    press = 2
                elif event.key == pygame.K_s:
                    arm2.angle_dx += 3.
                    grip.angle_dx += 3.
                    press = 2

                elif event.key == pygame.K_z:
                    arm3.angle_dx -= 3.
                    grip.angle_dx -= 3.
                    press = 3

                elif event.key == pygame.K_x:
                    arm3.angle_dx += 3.
                    grip.angle_dx += 3.
                    press = 3

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    arm1.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 1
                elif event.key == pygame.K_w:
                    arm1.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 1

                elif event.key == pygame.K_a:
                    arm2.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 2
                elif event.key == pygame.K_s:
                    arm2.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 2
                
                elif event.key == pygame.K_z:
                    arm3.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 3
                elif event.key == pygame.K_x:
                    arm3.angle_dx = 0.
                    grip.angle_dx = 0.
                    press = 3

                
        
        
        #2. logic
        arm1.update()        
        temp1 = (arm1.position[0] + L1 * np.cos(np.deg2rad(arm1.angle)), arm1.position[1] + L1 * np.sin(np.deg2rad(arm1.angle)))
        
        arm2.update(temp1)
        temp2 = (arm2.position[0] + L2 * np.cos(np.deg2rad(arm2.angle)), arm2.position[1] + L2 * np.sin(np.deg2rad(arm2.angle)))

        arm3.update(temp2)
        temp3 = (arm3.position[0] + L3 * np.cos(np.deg2rad(arm3.angle)), arm3.position[1] + L3 * np.sin(np.deg2rad(arm3.angle)))

        print(arm3.angle, temp3)
        print(arm3.position) 
        pygame.draw.circle(screen, (255,0,0), arm3.position, 3)
        
        
        if press == 1:
            grip.update2(arm1)
        if press == 2:
            grip.update2(arm2)
        if press == 3:
            grip.update1(arm3.position)

        #3. drawing
        screen.fill((250,250,250))
        arm1.draw(screen)
        pygame.draw.circle(screen, (0,0,0), First_Joint, 3)

        arm2.draw(screen)
        pygame.draw.circle(screen, (0,0,0), temp1, 3)

        arm3.draw(screen)
        pygame.draw.circle(screen, (0,0,0), temp2, 3)

        pygame.draw.circle(screen, (0,0,0), temp3, 3)

        grip.draw(screen)

        pygame.draw.circle(screen, (255,0,0), temp3, 3)
    
        pygame.display.flip()
        clock.tick(60)
    pass

if __name__ == "__main__":
    main()
