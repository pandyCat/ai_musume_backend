# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os
import openai
openai_api_key = os.getenv('OPEN_AI_KEY')
client = openai.OpenAI(api_key=openai_api_key)

# 鯖ポート番号
_port = os.getenv('API_SERVER_PORT')
_port = _port if _port!=None else 443
_host = str(os.getenv("PNDY_HOST"))
_host = _host if _host!=None else "0.0.0.0"

temp_wav_path = os.getenv("TENP_WAV_PATH")
temp_wav_path = temp_wav_path if temp_wav_path!=None else 'static'

# wav置くtempつくる
# 古いwavファイル消す
import shutil
if os.path.exists(temp_wav_path)==True:
    shutil.rmtree(temp_wav_path)
os.makedirs(temp_wav_path)

import persona

# ChatGPTにリクエストを送る
def replyGPTMessage(message):

  res = client.chat.completions.create(
      model="gpt-4o-mini",
      max_tokens=300,
      temperature=0.5,
      messages=persona.makoti(message)
  )
  print(res.choices[0].message)
  return res.choices[0].message


#---------------
# API 鯖
#---------------
import io

from flask import Flask, jsonify, send_file
from flask import request
from flask_cors import CORS

import delegate

app = Flask(__name__)
CORS(app)

def _processText(msg: str):
    resMsg = replyGPTMessage(msg)
    print(resMsg)

    #  emotion分析
    emotion_str = None
    emotion_str = delegate.analyzeEmotion(resMsg.content)
    emotion_str = emotion_str if emotion_str!=None else '嬉しい'    # emotion解析しないときはとりあえず '嬉しい'

    print("応答＝{0}, emotion={1}", resMsg.content, emotion_str)


    # 音声合成
    wavFileName = delegate.createVoice(resMsg.content, emotion_str, temp_wav_path)

    data = {"fileName": wavFileName,
            "emotion" : emotion_str,
            "resmsg"  : resMsg.content}

    return jsonify(data), 200


#   gptに投げて応答を得る
@app.route('/getResponse', methods=['POST'])
def getResponseFromText():
    msg = request.json["text"]
    return _processText(msg)

@app.route('/getResponseFromUnity', methods=['GET', 'POST'])
def getResponseFromUnity():
    msg = request.form['text']
    return _processText(msg)

## ファイル名->音声をバイナリで送信
@app.route("/audio", methods=['GET'])
def audio():
    
    # ファイル名
    wav_file_name = request.args.get('file_name')

    # 音声ファイルをバイト列で読み込む
    with open(f"{temp_wav_path}/{wav_file_name}", 'rb') as f:
        audio_data = f.read()

    # 音声ファイルをバイナリデータとして送信
    return send_file(io.BytesIO(audio_data),
      as_attachment=True,
      download_name=wav_file_name,
      mimetype='audio/wav')

#   # 疎通してるかどうかAPI
#   @app.route("/")
#   def index():
#       return "it is just a test or you shall die"

# python server.pyで鯖起動
if __name__=="__main__":
   app.run(debug=False, port=_port, host=_host)