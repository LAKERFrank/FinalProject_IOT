import numpy as np
import cv2
from gpiozero import Servo
import RPI.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BCM)

#micro switch part
GPIO.setup(27, GPIO.IN)
#count how many ball I make it
count=0

#servo part
servo_under=22
servo_upper=17
under=Servo(servo_under)
upper=Servo(servo_upper)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)

out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))

turn_l=False
turn_r=False
turn_c=False
under.mid()

while(True):
  #count people location
  count_l=0
  count_r=0
  count_c=0
  
  #upper servo close the gate
  upper.max()
  
  while(True):
    inputValue=GPIO.input(27)
    
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    print("1.boxes: ",boxes,"\nweight: ",weights)

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    print("\n2.boxes: ",boxes)

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
        if(xA<125):
          count_l+=1
        if(xB>500):
          count_r+=1
        if(xA>=125 and xB<=500):
          count_c+=1
    
    # Write the output video 
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if(count_l==15):
      turn_l=True
      break
    if(count_r==15):
      turn_r=True
      break
    if(count_c==15):
      turn_c=True
      break
    if inputValue==False:
      print("Button press")
      count+=1
  if(turn_l):
    under.max()
    printf("turn left")
    turn_l=False
    count_l=0
    count_r=0
    count_c=0
  if(turn_r):
    under.min()
    printf("turn right")
    turn_r=False
    count_l=0
    count_r=0
    count_c=0
  if(turn_c):
    under.mid()
    printf("turn to central")
    turn_c=False
    count_l=0
    count_r=0
    count_c=0

    
  time.sleep(2)
  under.mid()
  print("open")
  time.sleep(2)
  under.max()
  print("close") 
  print()
  
  print("count: ",count)
cap.release()
cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv2.waitKey(1)
