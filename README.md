# Fastiball: Auto ball return system
![](https://i.imgur.com/thcTYaY.png)

## 1. Introduction
### Why we need ball return system
In order to improve your game, you must devote a lot of time to practice. Dribbling, passing, and shooting are easy places to start practicing, and having a friend work out and improve their game alongside you is super rewarding. But what about those times when you have to get some shots up and no one is there to rebound for you?

ball return systems have been all the rage for well over two decades helping college and professional teams workout quicker and smarter.

### Who should get one
Any player who wants to improve their shot needs a good return system. While there’s nothing wrong with rebounding, being able to sit in one spot gives you better muscle memory from a certain area. It also allows you to get a better feel for an in-game shooting rhythm.

## 2. Fastiball
### motivation
I want to play basketball but pick up the ball that doesn't come to your way is the last thing I want to experience. And mostly I stay in dormitory. In that way, I would like to create some product that can solve my problem. That is Fastiball. 
### easier
Despite being a tremendous product with heavy weight and can only be used out door. Fastiball can be use indoor or even in the dormitory.

## 3. Require component
### Hardware
* Raspberry Pi 4
* NCS
* servo motor MG995
* servo motor SG90
* micro switch
* picamera
* T-cobbler
* 40P 彩虹排線
* water pipe
### Software
* python 3.7
* Open-Vino (4.1.2-openvino)
* Linebot
## 4. Tutorial
### servo motor
![](https://i.imgur.com/dWOgVwW.png)
* [gpiozero](https://www.raspberrypi-spy.co.uk/2018/02/basic-servo-use-with-the-raspberry-pi/)
![](https://i.imgur.com/R3juOVL.png)
    * For 90 degree:
    ```
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
    ```
    * For 180 degree:
    ```
    from gpiozero import Servo
    from time import sleep

    myGPIO=17

    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000

    servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)

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
    ```
* [gpio](https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/)
```
+90°：( 0.8 ms ／ 20 ms ) * 100 = 4
+60°：( 0.9 ms ／ 20 ms ) * 100 = 4.5
  0°：( 1.5 ms ／ 20 ms ) * 100 = 7.5
-60°：( 2.1 ms ／ 20 ms ) * 100 = 10.5
-90°：( 2.2 ms ／ 20 ms ) * 100 = 11
```
```
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
MotorPin=12
GPIO.setup(MotorPin,GPIO.OUT)
pwm_motor = GPIO.PWM(MotorPin, 50)
pwm_motor.start(7.5)                            #0°

while True:
        for a in range(100):
                pwm_motor.ChangeDutyCycle(4)    #+90°
                time.sleep(0.01)
                print a
#       pwm_motor.stop()
        for b in range(100):
                pwm_motor.ChangeDutyCycle(7.5)  #0°
                time.sleep(0.01)
                print b
#       pwm_motor.stop()
        for c in range(100):
                pwm_motor.ChangeDutyCycle(11)   #-90°
                time.sleep(0.01)
                print c
#       pwm_motor.stop()
        for d in range(100):
                pwm_motor.ChangeDutyCycle(7.5)  #0°
                time.sleep(0.01)
                print d
```
## Micro switch
![](https://i.imgur.com/1c3M5vW.png)

---

![](https://i.imgur.com/W1L2xHc.jpg)

---

On the right side of the upper picture is connect like this.
![](https://i.imgur.com/lwsLxQS.jpg)

---

![](https://i.imgur.com/2jTuXjF.jpg)
```
# import necessary library 匯入RPi.GPIO與time時間函式庫
import RPi.GPIO as GPIO   
import time   

# to use Raspberry Pi board pin numbers 使用板上定義的腳位號碼
GPIO.setmode(GPIO.BCM)   

# set up pin 11 as an output  將P1接頭的11腳位設定為輸入 
GPIO.setup(27, GPIO.IN)
count=0
# enter while loop unitl exit 隨著時間迴圈會重複執行，直到強制離開
while True:

# set up input value as GPIO.11 將P1接頭的11腳位的值設定為inputValue
    inputValue = GPIO.input(27)

# when user press the btn 如果是真 (玩家按下按鈕)
    if inputValue== False:

# show string on screen   顯示被按下
        print("Button pressed ")
        count+=1
        print("count: ",count)
        print()
#      while inputValue ==  False:  
# Set time interval as 0.3 second delay 設定延遲間隔為零點三秒鐘
        time.sleep(2)  
```

## People face detection
> reference:
> 1)[OpenVINO Toolkit](https://github.com/openvinotoolkit/open_model_zoo)
> 2)[Real-time Human Detection with OpenCV](https://thedatafrog.com/en/articles/human-detection-video/)
### Step 1. Accessing your webcam
There is an error when first time I operated cv2 with "sudo". If you encounter this problem as well, you can try to operate the same code without "sudo".
```
import numpy as np
import cv2

cv2.startWindowThread()
cap = cv2.VideoCapture(0)

while(True):
    # reading the frame
    ret, frame = cap.read()
    # displaying the frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break

cap.release()
cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv2.waitKey(1)
```
### Step 2. People detection with HOG
```
# import the necessary packages
import numpy as np
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    
    # Write the output video 
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
```
## T-cobbler&40P 彩虹排線
By using this two, you can use "Dupont Line" to connect with other components easier than on raspi.
![](https://i.imgur.com/isP8ZgK.jpg)


---

![](https://i.imgur.com/Ffv35Bm.jpg)


## 5. Demo
* [Servo_baffle Test](https://youtu.be/iG8yXcTiKDs)
    * To stuck the ball until spin is complete
* [Micro Switch Test](https://youtu.be/kuMZI8M_fRk)
    * To count how many ball I make it
* [Micro switch & Servo_baffle Combine Test](https://youtu.be/FsahKTZwoSs)
    * To count how many ball I make it and open the gate
* Recognize people with picamera
* Completed Fastiball

