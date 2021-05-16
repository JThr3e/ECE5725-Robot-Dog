from flask import Flask
import os
import time
from adafruit_servokit import ServoKit
import pygame
from pygame.locals import *
from collections import deque
import sys
import threading

#Sets up pygame
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#History
history = deque([' ', ' ', ' ', ' ', ' '])

#Panic stop boolean variable
stop = False

app = Flask(__name__)
pid = None
#<img style="-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="http://jo3.cc:8081/" width="641" height="360">
#888 499
webpage=\
"""
<!--
<style>
img {
display:inline-block;
  }
</style> 
<img class="shrinkToFit" src="http://jo3.cc:8081/" alt="http://jo3.cc:8081/" width="426" height="240"></img>
<img class="shrinkToFit" src="http://jo3.cc:8042/video.mjpg" alt="http://jo3.cc:8042/video.mjpg" width="426" height="240"></img>
-->
<img class="shrinkToFit" src="http://jo3.cc:8081/" alt="http://jo3.cc:8081/" width="888" height="499"></img>
<br>
<body>
<h1><a href="/forward">Forward</a></h1><h1><a href="/backward">Backward</a></h1>
<h1><a href="/turn_left">Turn Left</a></h1><h1><a href="/turn_right">Turn Right</a></h1>
<h1><a href="/set_neutral">Neutral</a></h1>
</body>
"""
use = False #True is in use, False is not in use

@app.route('/')
def hello_world():
    return webpage

@app.route('/forward')
def forward():
    global use
    if (not use):
        use = True
        print("forward!")
        go_forward()
        use = False
    else:
        print("Busy")  
    return webpage

@app.route('/turn_left')
def turn_left_web():
    global use
    if (not use):
        use = True
        print("turn left!")
        turn_left()
        use = False
    else:
        print("Busy")
    return webpage

@app.route('/turn_right')
def turn_right_web():
    global use
    if (not use):
        use = True
        print("turn right!")
        turn_right()
        use = False
    else:
        print("Busy")
    return webpage

@app.route('/set_neutral')
def neutral():
    global use
    if (not use):
        use = True
        print("set neutral position!")
        set_neutral()
        use = False
    else:
        print("Busy")
    return webpage

@app.route('/backward')
def backward():
    global use
    if (not use):
        use = True
        print("backward!")
        go_backward()
        use = False
    else:
        print("Busy")
    return webpage

print("starting...") 

kit = ServoKit(channels=16)

"""NEUTRAL POSITION"""
#          0   1   2  3  4   5  10  11  12  13  14  15
stand   = [50,80,80,80,140,100,130,140,80,100,90,100]


"""FORWARD CONFIGS"""
#                               0   1   2   3   4   5  10  11  12  13  14  15
diagonal_FLBR =              [  0, 20,-10,  0, 30, 30,-20,-50,  0,  0,-40,  0]
diagonal_FLBR_back =         [  0, 20, 20,  0, 30, 30,-20,-50, 20,  0,-40,  0]
diagonal_FLBR_back_forward = [-30, 20, 20, 20,-30, 30, 40,-50, 20,  0,-40, 30]
diagonal_FRBL      =         [-30,  0,-10,  0,-30,-30, 40, 30,  0,  0,  0, 40]
diagonal_FRBL_back =         [-30,  0,-10,-30,-30,-30, 40, 30,  0,-20,  0, 40]
diagonal_FRBL_back_forward = [-30, 20,-10,-30,-30, 30, 40,-40,  0,-20,-30, 40] 

"""RIGHT CONFIGS"""
#                               0   1   2   3   4   5  10  11  12  13  14  15
l_diagonal_FLBR =              [  0, 20,  0,  0,  0, 30,-20,  0,  0,  0,  0,  0]
l_diagonal_FLBR_back =         [  0, 20,  0,  0,  0, 30,-20,  0, 20,  0,  0,  0]
l_diagonal_FLBR_back_forward = [  0, 20,  0, 20,  0, 30, 40,  0, 20,  0,  0, 30]
l_diagonal_FRBL      =         [  0,  0,  0,  0,  0,-30, 40,  0,  0,  0,  0, 40]
l_diagonal_FRBL_back =         [  0,  0,  0,-30,  0,-30, 40,  0,  0,  0,  0, 40]
l_diagonal_FRBL_back_forward = [  0, 20,  0,-30,  0, 30, 40,  0,  0,  0,  0, 40] 

"""LEFT CONFIGS"""
#                               0   1   2   3   4   5  10  11  12  13  14  15
r_diagonal_FLBR =              [  0,  0,-10,  0, 30,  0,  0,-50,  0,  0,-40,  0]
r_diagonal_FLBR_back =         [  0,  0, 20,  0, 30,  0,  0,-50,  0,  0,-40,  0]
r_diagonal_FLBR_back_forward = [-30,  0, 20,  0,-30,  0,  0,-50,  0,  0,-40,  0]
r_diagonal_FRBL      =         [-30,  0,-10,  0,-30,  0,  0, 30,  0,  0,  0,  0]
r_diagonal_FRBL_back =         [-30,  0,-10,  0,-30,  0,  0, 30,  0,-20,  0,  0]
r_diagonal_FRBL_back_forward = [-30,  0,-10,  0,-30,  0,  0,-40,  0,-20,-30,  0] 

"""RIGHT 2 CONFIGS"""
#                                  0   1   2   3   4   5  10  11  12  13  14  15
r2_diagonal_FLBR =              [ 20, 20,-10,  0, 30, 30,-20,-20,  0,  0,  0,  0]
r2_diagonal_FLBR_back =         [ 20, 20,-10,  0, 30, 30,-20,-20, 20,-20,  0,  0]
r2_diagonal_FLBR_back_forward = [ 20, 20,-10, 20, 30, 30, 40, 20, 20,-20, 20, 30]
r2_diagonal_FRBL      =         [  0,  0,-10,  0,-20,-30, 40, 20,  0,  0, 20, 40]
r2_diagonal_FRBL_back =         [  0,  0, 10,-30,-20,-30, 40, 20,  0,  0, 20, 40]
r2_diagonal_FRBL_back_forward = [ 20, 20, 10,-30, 30, 30, 40, 20,  0,  0, 20, 40] 

"""LEFT 2 CONFIGS"""
#                                  0   1   2   3   4   5  10  11  12  13  14  15
l2_diagonal_FLBR =              [  0,  0,-10,  0, 30, 15,-20,-50,-10,  0,-40,-20]
l2_diagonal_FLBR_back =         [  0,  0, 20,-20, 30, 15,-20,-50,-10,  0,-40,-20]
l2_diagonal_FLBR_back_forward = [-30,-20, 20,-20,-30,-25,-20,-50,-10,  0,-40,-20]
l2_diagonal_FRBL      =         [-30,-20,-10,  0,-30,-25, 10, 30,-10,  0,  0,  0]
l2_diagonal_FRBL_back =         [-30,-20,-10,  0,-30,-25, 10, 30, 10,-20,  0,  0]
l2_diagonal_FRBL_back_forward = [-30,-20,-10,  0,-30,-25,-20,-40, 10,-20,-30,-20] 

"""BACKWARD CONFIGS"""
#0-BLL, 1-BLR, 2-BSL , 3-BSR, 4-BUL 5-BUR  ,10-FUR, 11-FUL, 12-FSR, 13-FSL, 14-FLL, 15-FLR
#                              0   1   2   3   4   5  10  11  12  13  14  15
reverse_FLBR =              [ 20,  0,-10,  0, 30, 15,-20,-20,-10,  0,  0,-20]
reverse_FLBR_back =         [ 20,  0,-10,-20, 30, 15,-20,-20,-10,-20,  0,-20]
reverse_FLBR_back_forward = [ 20,-20,-10,-20, 30,-25,-20, 20,-10,-20, 20,-20]
reverse_FRBL      =         [  0,-20,-10,  0,-20,-25, 10, 20,-10,  0, 20,  0]
reverse_FRBL_back =         [  0,-20, 10,  0,-20,-25, 10, 20, 10,  0, 20,  0]
reverse_FRBL_back_forward = [ 20,-20, 10,  0, 30,-25,-20, 20, 10,  0, 20,-20] 

#takes in a configuration offset, a neutral position and 
#   number of steps to get to the new offset
def set_legs(offset, stand, steps):
    global stop
    offset_stand = list(zip(offset, stand))
    movement = [(0,0)]*16
    for i, angles in enumerate(offset_stand):
        if i > 5:   
            i+=4
        old_move = int(kit.servo[i].angle)
        new_move = angles[0] + angles[1]
        step = (new_move-old_move)/steps
        movement[i] = (old_move, step) 
    #smoothly transition from one configuration to the next     
    for i in range(0,steps):
        for j, angles in enumerate(movement):
            if j <= 5 or j >= 10:
                #update servo position
                while (stop == True):
                    time.sleep(0.5)
                try:
                    kit.servo[j].angle = angles[0]
                except IOError:
                    print("IO Error")
        for j in range(0,len(movement)):
            if j <= 5 or j >= 10:
                #increment positions based on step
                movement[j] = (movement[j][0]+movement[j][1], movement[j][1])
        time.sleep(0.01)


def set_neutral():
    history.append('NEUTRAL')
    history.popleft()
    for i in range(0, len(stand)):
        angle = stand[i]
        if i > 5:
            i+=4
        kit.servo[i].angle = angle
    time.sleep(0.5)

set_neutral()
time.sleep(0.5)
def go_backward():
    history.append('BACKWARD')
    history.popleft()
    set_legs(reverse_FLBR, stand, 10)
    set_legs(reverse_FLBR_back, stand, 10)
    set_legs(reverse_FLBR_back_forward, stand, 10)
    set_legs(reverse_FRBL, stand, 40)
    set_legs(reverse_FRBL_back, stand, 10)
    set_legs(reverse_FRBL_back_forward, stand, 10)
    set_legs(reverse_FLBR, stand, 40)
    set_legs([0]*12,stand,10)

def go_forward():
    history.append('GO FORWARD')
    history.popleft()
    set_legs(diagonal_FLBR,stand,10)           
    set_legs(diagonal_FLBR_back,stand,10)
    set_legs(diagonal_FLBR_back_forward,stand,10)
    set_legs(diagonal_FRBL,stand,40)
    set_legs(diagonal_FRBL_back,stand,10) 
    set_legs(diagonal_FRBL_back_forward,stand,10) 
    set_legs(diagonal_FLBR,stand,40)           
    set_legs([0]*12,stand,10)           

def turn_right():
    history.append('TURN RIGHT')
    history.popleft()
    set_legs(r2_diagonal_FLBR,stand,10)           
    set_legs(r2_diagonal_FLBR_back,stand,10)
    set_legs(r2_diagonal_FLBR_back_forward,stand,10)
    set_legs(r2_diagonal_FRBL,stand,40)
    set_legs(r2_diagonal_FRBL_back,stand,10) 
    set_legs(r2_diagonal_FRBL_back_forward,stand,10) 
    set_legs(r2_diagonal_FLBR,stand,40)           
    set_legs([0]*12,stand,10)           

def turn_left():
    history.append('TURN LEFT')
    history.popleft()
    set_legs(l2_diagonal_FLBR,stand,10)           
    set_legs(l2_diagonal_FLBR_back,stand,10)
    set_legs(l2_diagonal_FLBR_back_forward,stand,10)
    set_legs(l2_diagonal_FRBL,stand,40)
    set_legs(l2_diagonal_FRBL_back,stand,10) 
    set_legs(l2_diagonal_FRBL_back_forward,stand,10) 
    set_legs(l2_diagonal_FLBR,stand,40)           
    set_legs([0]*12,stand,10)

def pygame_loop():
    pygame.init()
    pygame.mouse.set_visible(False)
    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    YELLOW = 255, 255, 0
    my_font = pygame.font.Font(None, 15)
    stop_surface = my_font.render('STOP', True, WHITE)
    stop_rect = stop_surface.get_rect(center = (40, 120))
    resume_surface = my_font.render('RESUME', True, WHITE)
    resume_rect = resume_surface.get_rect(center = (40, 120))
    quit_surface = my_font.render('QUIT', True, BLACK) 
    quit_rect = quit_surface.get_rect(center = (280, 120)) 
    global stop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type is pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #QUIT button pressed
                if (x > 240) and (x < 320) and (y > 80) and (y < 160):
                    pygame.quit()
                    os.kill(pid,9) 
                    exit()
                #RESUME/STOP button pressed
                if (x > 0) and (x < 80) and (y > 80) and (y < 160):
                    stop = not stop
        #Screen display
        screen.fill(BLACK)
        pygame.draw.circle(screen, YELLOW, (280, 120), 40)
        screen.blit(quit_surface, quit_rect)
        #Update history
        for i in range(len(history)):
            text_surface = my_font.render(str(history[i]), True, WHITE)                
            rect = text_surface.get_rect(center = (160, 60 + i*25))
            screen.blit(text_surface, rect)
        #STOP button pressed
        if (stop):
            pygame.draw.circle(screen, GREEN, (40, 120), 40)
            screen.blit(resume_surface, resume_rect)
        #RESUME button pressed
        else:
            pygame.draw.circle(screen, RED, (40, 120), 40)
            screen.blit(stop_surface, stop_rect)
        pygame.display.flip()


if __name__ == '__main__':
    pid = os.getpid()
    t = threading.Thread(target =pygame_loop, args =())
    t.start()
    app.run(host='0.0.0.0', port=5000)

