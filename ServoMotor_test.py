#move from 0 to 90 degree with 2 step
from gpiozero import Servo
from time import sleep

myGPIO=17

servo = Servo(myGPIO)

while True:
    way=input("left or right or central(l for left,r for right,c for central)?")
    if(way=="l"):
        servo.max()
        print("left")
    elif(way=="r"):
        servo.min()
        print("right")
    elif(way=="c"):
        servo.mid()
        print("central")
    else:
        break
