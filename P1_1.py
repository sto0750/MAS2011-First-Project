#clock
import pygame
import numpy as np
import time


WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650
Center = (WINDOW_WIDTH/2. , WINDOW_HEIGHT/2.)

pygame.init()
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
clock = pygame.time.Clock()

# laod alarm bell ==============================================
name = "assets/alarm.wav"
alarm = pygame.mixer.Sound(name)

# functions ====================================================
def getrectangle(width, height, x=0, y=0):
    v = np.array([ [x,y], [x+width, y], [x+width, y+height], [x, y+height]])
    diff = [-height/2. , -height/2.]  # renew the rotating axis
    v = v + diff
    return v

def Rmat(deg):
    rad = np.deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array( [[c, -s, 0]
                  ,[s,  c, 0]
                  ,[0,  0, 1]])
    return R

def Tmat(tx, ty):
    T = np.array( [[1,0,tx], [0,1,ty], [0,0,1]], dtype='float')
    return T



# classes ======================================================
class Arrow():
    def __init__(self,width, height, angle):
        self.width = width
        self.height = height
        rect = getrectangle(width, height, x=Center[0], y=Center[1])

        M = Tmat(Center[0], Center[1]) @ Rmat(angle-90) @ Tmat(-Center[0], -Center[1])
        R = M[0:2, 0:2]
        t = M[0:2, 2]    #making the initial angle (when starting)

        self.p = (R @ rect.T).T + t

    
    def update(self, Matrix):
        R = Matrix[0:2, 0:2]
        t = Matrix[0:2, 2]

        self.p = (R @ (self.p.T)).T + t
    
    def draw(self, screen, color):
        pygame.draw.polygon(screen, color, self.p)




# main function ================================================
def main():
        # calculating the current time when the program starts
    T = time.gmtime()
    h = (T.tm_hour + 9) % 24
    m = T.tm_min
    s = T.tm_sec

        # calculating the initial angle of each needle according to the current time
    degS = s * 6.
    degM = m * 6. + s / 10.
    degH = h * 30. + m / 2. + s / 120.
    
        # make each needle according to the angle
    Hour = Arrow(120,17, angle = degH)
    Minute = Arrow(300,8, angle = degM)
    Second = Arrow(250,5, angle = degS - 12) # little correction

    refreshrate = 1

    done = False
    while not done:
        # 1 event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        # 2 logic
        
            #rotating each needle with proper speed
        matS = Tmat(Center[0], Center[1]) @ Rmat(6/(refreshrate)) @ Tmat(-Center[0], -Center[1])
        matM = Tmat(Center[0], Center[1]) @ Rmat(6/(refreshrate*60)) @ Tmat(-Center[0], -Center[1])
        matH = Tmat(Center[0], Center[1]) @ Rmat(6/(refreshrate*60*12)) @ Tmat(-Center[0], -Center[1])

            #update means applying the rotation matrix
        Second.update(matS)
        Minute.update(matM)
        Hour.update(matH)

            # At every hour an alarm bell rings
        if time.gmtime().tm_min == 0 and time.gmtime().tm_sec == 0:
            alarm.play()

        # 3 draw
        screen.fill((255,255,255))
            # drawing index
        for i in range(1,13):
            direction = np.array([np.cos(2*np.pi*i/12), np.sin(2*np.pi*i/12)])
            pygame.draw.line(screen, (0,0,0), 305 * direction + Center , 310 * direction + Center, width=6)

            # drawing clock needles
        Second.draw(screen, (255,0,0))
        Minute.draw(screen, (0,0,0))
        Hour.draw(screen, (66, 96, 245))

            #pointing the center
        pygame.draw.circle(screen, (0,0,0), Center, 10)

            #check if the seconds are accurate
        print(time.gmtime().tm_sec)  

        # 4
        pygame.display.flip()
        clock.tick(refreshrate)          
    pass

flag = False
while not flag:
    if time.time() - int(time.time()) < 0.001:    #start when the milliseconds are small enough
        flag = True
        main()
    
