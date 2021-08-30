import os

from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort, render_template


app = Flask(__name__)

Channel_Access_Token = ''
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = ''
handler = WebhookHandler(Channel_Secret)


# handle request from "/callback" 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body      = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# handle text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if 'quick' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='a quick reply message',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=CameraAction(label="開啟相機吧")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="相機膠捲")
                        ),
                        # return a location message
                        QuickReplyButton(
                            action=LocationAction(label="位置資訊")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="postback", data="postback")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="message", text="one message")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="時間選單",
                                                        data ="date_postback",
                                                        mode ="date")
                        )
                    ])))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )


# Handle PostbackEvent
@handler.add(PostbackEvent)
def handle_message(event):
    data = event.postback.data
    if data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
