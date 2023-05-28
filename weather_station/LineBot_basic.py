# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import DAN
import random

line_bot_api = LineBotApi('0PpNV9CO0HrIDNnVXd1qPGGH6UEKYcrnKQz+Qkz+4+Sp3cfI6ollfA+JravkIhTfKdipZCaHmpwL3lZuAed4L'
                          '//lx1muIyJ6fqK3yj4z2IK9A452nxNaQFosHw3kXhXodwz+9gOJVS70ODN+LvPh3gdB04t89/1O/w1cDnyilFU=')
#LineBot's Channel access token
handler = WebhookHandler('1788a720f740e60ba0fec792a1fa6338')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)

ServerURL = 'https://2.iottalk.tw'

Reg_addr = None

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name'] = "陳彥廷_" + str(random.randint(100, 999)) + "_" + DAN.profile['dm_name']  # None

DAN.device_registration_with_retry(ServerURL, Reg_addr)


def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))

    if Msg == 'temp':
        while True:
            temp = DAN.pull('Dummy_Control')
            if temp:
                break
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Temperature: {}'.format(temp[0])))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='收到訊息！'))

    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

   
if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    

