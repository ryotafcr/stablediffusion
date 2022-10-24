from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage,ImageSendMessage
)
from googletrans import Translator
import imageupload
import stablediffusion

app = Flask(__name__)

line_bot_api = LineBotApi('f1sEoI15SNpuGfKO5x4CpFLJ3y7QGFqqcGVdGIxJtPRdb+pz+uRarTeX6Kx+xtTt4JJDkUgXzatPoE6D9CeTv0S22PZqjmTMAS4AxT54U6iXi5A7VYcJAMjSO2pQk/KDaqCUH9a9oKuUiOGrVUsO3wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e49d669eec66ca833a9a52b34d2349cd')

@app.route("/")
def test():
    return "OK"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))
    translator = Translator()
    translated = translator.translate(event.message.text)
    prompt = translated.text
    
    # stablediffusion
    stablediffusion.stablediffusion(prompt)
    
    # driveに作成された画像をuploadしてidを取り出す
    fid = imageupload.id()
    # print(f['id'])
    
    url = "https://drive.google.com/uc?export=view&id=" + str(fid)
    print(url)
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url= url ,
            preview_image_url= url ))
    
    
if __name__ == "__main__":
    app.run()