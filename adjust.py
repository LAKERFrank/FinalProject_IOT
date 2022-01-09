from gpiozero import Servo
import RPI.GPIO as GPIO
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
app = Flask(__name__)
line_bot_api = LineBotApi('Channel Access token')
handler = WebhookHandler('Channel Secret')

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
GPIO.setmode(GPIO.BCM)
servo_under=22
servo_upper=17
under=Servo(servo_under)
upper=Servo(servo_upper)
upper.max()

# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if(msg=="關"):
        upper.max()
    if(msg=="開"):
        upper.mid()
    if(msg=="左"):
        under.max()
        sleep(1)
        upper.mid()
        sleep(1)
        upper.max()
    if(msg=="中"):
        under.mid()
        sleep(1)
        upper.mid()
        sleep(1)
        upper.max()
    if(msg=="右"):
        under.min()
        sleep(1)
        upper.mid()
        sleep(1)
        upper.max()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = msg))

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566)
