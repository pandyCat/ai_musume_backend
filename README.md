# AI娘バックエンド

AI娘 バックエンドです

# 実行法

```
python server.py
```

# please note

Please Note that
You have to implement the generation function with the following interface to generate a voice
```
def makeSomeNoise(speakText:str, emotion_str:str, temp_wav_path:str) -> str:
```

The makeSomeNoise() function must generate a high quality voice and return it.
This repository does not include any generation functions or voice.py.

# setup .env

please setup .env file in the home directory like this:

```
OPEN_AI_KEY=YOUR_OPENAI_KEY
API_SERVER_PORT=YOUR_PORT
TENP_WAV_PATH=static
PNDY_HOST=0.0.0.0
```