import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('vijUy1ucBU4o6P/rgXBZIn3vELqQwkFca8KSYpSwaLMoT0dk3OHLFjkOONe4HCp+px6FzsV1zbhi6X8e58u78hvjjJ/n8/zS4D4KwWCkQWpvBX6R6xFfVNcB6b4AtHtoxZZV4iyISxR3uUmwab/3PQdB04t89/1O/w1cDnyilFU=
')
handler = WebhookHandler('2ce6f55a0194c7e4f1d9e50ff06ba64f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
