import  RPi.GPIO as GPIO
from time import sleep

width, height = 640,480
l_motor = 2
left_front   =  4
left_back   =  3
 
r_motor = 24
right_front   = 18
right_back  =  23
 
 
def Motor_Init():
    global L_Motor, R_Motor
    L_Motor= GPIO.PWM(l_motor,100)
    R_Motor = GPIO.PWM(r_motor,100)
    L_Motor.start(0)
    R_Motor.start(0)
 
 
def Direction_Init():
    GPIO.setup(left_back,GPIO.OUT)
    GPIO.setup(left_front,GPIO.OUT)
    GPIO.setup(l_motor,GPIO.OUT)
    
    GPIO.setup(right_front,GPIO.OUT)
    GPIO.setup(right_back,GPIO.OUT)
    GPIO.setup(r_motor,GPIO.OUT)
    
 
def Init():
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    Direction_Init()
    Motor_Init()
 
 
def Back(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front,1)   #left_front
    GPIO.output(left_back,0)    #left_back
 
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front,1)  #right_front
    GPIO.output(right_back,0)   #right_back
     
    
def Front(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front,0)   #left_front
    GPIO.output(left_back,1)    #left_back
 
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front,0)  #right_front
    GPIO.output(right_back,1)   #right_back
 
 
def Left(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front,0)   #left_front
    GPIO.output(left_back,1)    #left_back
 
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front,1)  #right_front
    GPIO.output(right_back,0)   #right_back
 
 
def Right(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front,1)   #left_front
    GPIO.output(left_back,0)    #left_back
 
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front,0)  #right_front
    GPIO.output(right_back,1)   #right_back
 
 
def Stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(left_front,0)   #left_front
    GPIO.output(left_back,0)    #left_back
 
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(right_front,0)  #right_front
    GPIO.output(right_back,0)   #right_back
 
def Move(x,y):
    global second
    #stop
    if x==0 and y==0:
        Stop()
    #go ahead
    elif width/3 <x and x<(width-width/3):
        Front(70)
        sleep(0.1)
        Stop()
    #left
    elif x < width/3:
        print("x")
        Left(70)
        sleep(0.1)
        Stop()
    #Right
    else :
        Right(70)
        sleep(0.1)
        Stop()
'''def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm_servo.set_pwm_freq(50)                #frequency==50Hz (servo)
    pwm_servo.set_pwm(channel,0,int(angle))'''

