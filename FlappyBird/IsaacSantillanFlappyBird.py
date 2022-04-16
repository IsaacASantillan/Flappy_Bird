# To play the game hit the green playbutton in Visual Studio Code 
# Start up pygame and import needed libraries 
import pygame
from pygame.locals import *
import random

        
#Set up Pygame so you can Quit if you want 
def events():
   for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()
 
# Define Display Screen, Width, and Height           
W, H = 864, 936


#Define Colors 
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
BLACK=(0,0,0)
WHITE=(255,255,255)

 
# Setup pygame
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
vec=pygame.math.Vector2
FPS = 120


#Set Game Font/Set Score to Zero  
font=pygame.font.SysFont('Comic Sans MS.ttf',150)
score=0



#Set Background 
bkgd = pygame.image.load("flappybg.png").convert()
x=0

#Set Pipe Gap/Frequency 
pipe_gap=200 
pipe_frequency=1500 #milliseconds 

# pygame.time.get_()ticks Takes a measure of time once the game has started. Subtract this by the pipe_frequency
#.... by the pipe_frequency to get the time the last_pipe is generated 
last_pipe=pygame.time.get_ticks()-pipe_frequency

#Set Fireball Gap/Frequency 
fireball_gap=400
fireball_frequency=1500 
last_fireball=pygame.time.get_ticks()
 

#Sprite Class
class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #loads sprite image
        self.image=pygame.image.load("spritey.png").convert()
        #Make black background of sprite image clear 
        self.image.set_colorkey(BLACK)
        #Make imaginary rectangle around sprite
        self.rect=self.image.get_rect()
        #Starting Position of Sprite
        self.pos=vec(100,400)
        #Set your sprite jump velocity/acceleration both vertically and horizontally  
        self.vel=vec(0,0)
        self.acc=vec(0,0)
    
    def update(self):        
        self.vel+=self.acc
        self.pos+=self.vel+(self.acc)/9 
        self.rect.center=self.pos 
#Create a Flapp group 
Flappy_group=pygame.sprite.Group()
flappy=Flappy()
#Create an instance of flappy
Flappy_group.add(flappy)


#Pipes Class
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        #Add extra input where if position == 1 then the pipe will be flipped using the transform function
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True) or flappy.rect.x<864
            self.rect.bottomleft=[x,y-int(pipe_gap/1.8)]
        if position==-1:
            self.rect.topleft=[x,y+int(pipe_gap/1.8)]
    #Subtract Pipe x position by 5 which makes it move to the left 
    def update(self):
        self.rect.x-=5 
#Create a pipe Group 
pipe_group=pygame.sprite.Group()

# Fireball Class
class Fireball(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("firey.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
    #Add extra input where if position == 1 then the pipe will be on the bottom left if position ==-1 then the fireball
    #...will be on the top left 
        if position==1:
            self.rect.bottomleft=[x,y-int(fireball_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y+int(fireball_gap/2)]
    #Subract x position by 7 which makes it move to the left faster than the pipes 
    def update(self):
        self.rect.x -=7                     
        
fireball_group=pygame.sprite.Group()


#Functions
# Function that is used to see if time - time2 > freq which we will use to know when to generate the next pipe 
def addnow(time,time2,freq):
    if time-time2>freq:
        return True 
    else:
        return False 
#Functon that is used to see that if we reach the end of our background to keep scrolling it left 
def bgpos(x,y):
    if x<y:
        return True
    else:
        return False 

 
# Main Game Loop 

game_start=False 
run=True
while run:
    CLOCK.tick(FPS)
    time_now=pygame.time.get_ticks()

    #Scrolling Background
    #Divides x by width of bkgd images and gives remainder to indicate where the bkgd image ends 
    old_pos = x%bkgd.get_rect().width
    #Makes it so that first image is diplayed and then makes sure python knows that old_pos is where the bkgd image ends 
    DS.blit(bkgd, (old_pos - bkgd.get_rect().width, 0))
    # makes surethat if old_pos is less than our display surface width then we can add the background image again after to make it seem 
    # as though it is never ending  
    if bgpos(old_pos,W):
        DS.blit(bkgd, (old_pos, 0))
    #how fast the scrolling background moves 
    x -= 5




    #Add Pipes
    #if time_now(How much time the game has been running)-last_pipe(the time the first pipe is created) is greater than
    #..the pipe frequency then we can add an extra pipe
    if addnow(time_now,last_pipe,pipe_frequency):
        #the ranint function chooses a random number between two integers which we use to randomly generate the bottom 
        # ...and top pipe heights to make the game harder  
        pipe_height=random.randint(-200,160)
        #where to draw the pipes on the screen 
        btm_pipe=Pipe(W,int(H/2)+pipe_height,-1)
        top_pipe=Pipe(W,int(H/2)+pipe_height,1)
        #adds instances to pipe group
        pipe_group.add(btm_pipe)
        pipe_group.add(top_pipe)
        #resets the timer 
        last_pipe=time_now
    #Draws the pipes on the screen and updates the screen 
    pipe_group.draw(DS)
    pipe_group.update()



    #Add Fireballs 
    if addnow(time_now,last_fireball,fireball_frequency):
        fireball_height=random.randint(-200,300)
        btm_fireball=Fireball(W-fireball_height,int(H/2)+fireball_height,-1)
        top_fireball=Fireball(W+fireball_height,int(H/2)+fireball_height,1)
        fireball_group.add(btm_fireball)
        fireball_group.add(top_fireball)
        last_fireball=time_now
    fireball_group.draw(DS)
    fireball_group.update()


    #Space Bar to increase/decrease flappy bird height + Add Score 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
            #every space bar decreases the y coordinate which makes the flappy bird "jump" and every space bar hit also increases the
            #..score by one 
                flappy.vel.y=-3.95 
                flappy.acc.y=+0.1
                score+=1
                
            

    #Display Score on Screen
    DS.blit(font.render(str(score),True,blue),(H/2,100)) 
        

    #Collide Feature/quits the game 
    #We used the group collide function to show that if the flappy bird hits below the height of the screen to quit the game or if it
    # ...hits one of the pipes or fireballs 
    if pygame.sprite.groupcollide(Flappy_group,pipe_group,False,False) or flappy.pos.y>=864 or pygame.sprite.groupcollide(Flappy_group,fireball_group,False,False) :
        run=False


    # Update Flappy Bird Position + Screen 
    Flappy_group.update()
    Flappy_group.draw(DS)
    pygame.display.update()

    