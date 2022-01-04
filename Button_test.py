# import necessary library 匯入RPi.GPIO與time時間函式庫
import RPi.GPIO as GPIO   
import time   

# to use Raspberry Pi BCM pin numbers 使用板上定義的腳位號碼
GPIO.setmode(GPIO.BCM)   

# set up pin 27 as an output  將P1接頭的27腳位設定為輸入 
GPIO.setup(27, GPIO.IN)
# use to count how many ball enter  計算球數
count=0

# enter while loop unitl exit 隨著時間迴圈會重複執行，直到強制離開
while True:

# set up input value as GPIO.27 將P1接頭的27腳位的值設定為inputValue
    inputValue = GPIO.input(27)

# when user press the btn 如果是真 (玩家按下按鈕)
    if inputValue== False:

# show string on screen  顯示被按下
        print("Button pressed ")
# number of ball make it inc  進球數+1
        count+=1
# show count on screen  顯示進球數
        print("count: ",count)
        print()

# Set time interval as 2 second delay 設定延遲間隔為零點三秒鐘
        time.sleep(2)  
