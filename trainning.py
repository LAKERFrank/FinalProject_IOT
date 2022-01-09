from gpiozero import Servo
import RPi.GPIO as GPIO
from time import sleep
import time
# import flask related
from flask import Flask, request, abort
from urllib.parse import parse_qsl
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)
import json
# create flask server
app = Flask(_name_)
line_bot_api = LineBotApi('So7/ZBDVTz8ZPEEmDOESo2hq9Ybw3dwtCgATe8haU+AajMq28KPPI/fdi7uVU9eX1N6z56MOWzN0VPmDEZsw5oPiE+9iRN1ufkAGg0yU/lFd3J0yXaz2gyLY1tVhirx2nnsdNtNjJtBo+dWJ8Boj3QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a9a92c747e92845282dd8426884a51e3')
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'
#servo part
GPIO.setmode(GPIO.BCM)
servo_under=22
servo_upper=17
under=Servo(servo_under)
upper=Servo(servo_upper)
upper.max()

practice1=["l","r","c","l","r","l",]  #菜單一
practice2=["r","c","r","l","c","l",]  #菜單二
practice3=["c","l","r","l","c","r",]  #菜單三

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    msg = event.message.text
    if(msg=="P1"):
        sleep(2)
        for p in practice1:
            if p =="l":
                under.max()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            elif p=="c":
                under.mid()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            else:
                under.min()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
    if(msg=="P2"):
        sleep(2)
        for p in practice2:
            if p =="l":
                under.max()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            elif p=="c":
                under.mid()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            else:
                under.min()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
    if(msg=="P3"):
        sleep(2)
        for p in practice3:
            if p =="l":
                under.max()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            elif p=="c":
                under.mid()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
            else:
                under.min()
                sleep(1)
                upper.mid()
                sleep(1)
                upper.max()
                sleep(2)
    under.mid()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "done"))


if _name_ == "_main_":
    app.run(host='0.0.0.0', port=80)
