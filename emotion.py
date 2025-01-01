#   感情分析

#from mlask import MLAsk
import os
from asari.api import Sonar

# mecab_path = r"C:\Program Files\MeCab\dic\ipadic"
# #mecab_arg = "-d " + mecab_path
# emotion_analyzer = MLAsk()
# #emotion_analyzer = MLAsk(mecab_arg=mecab_path)

sonar = Sonar()


def analyze_emotion(message:str) -> str:

    emotion = sonar.ping(text=message)
    #print(result)
    #print("negative={0} and positive={1}".format(result['classes'][0]['confidence'], result['classes'][1]['confidence']))

    #https://cevio.jp/guide/cevio_ai/interface/com/
    #例2『マコチ』→ "嬉しい", "普通", "怒り", "哀しみ", "落ち着き"

    # 0=negative度 1=positive度
    emotion_map_positive = [
        [1, 0.66 ,'嬉しい'],
        [1, 0.33 ,'普通'],
    ]
    emotion_map_negative = [
        [0, 0.66 ,'哀しみ'],
        [0, 0.33 ,'怒り'],
    ]
    emotion_map_normal = [
        [1, 0.0 ,'落ち着き'],
    ]

    #   ['classes'][1]['confidence']はpositive要素
    #   ['classes'][0]['confidence']はnegative要素
    for emotion_p in emotion_map_positive:
        if emotion['classes'][1]['confidence'] >= emotion_p[1]:
            return emotion_p[2] # 
    
    for emotion_n in emotion_map_negative:
        if emotion['classes'][0]['confidence'] >= emotion_n[1]:
            return emotion_n[2]

    return emotion_map_normal[0][2]


# 単体テスト
if __name__=="__main__":

    test_sentence = [
       "'彼女のことが嫌いではない！(;´Д`)'",
       "あなたのことが大好きです！",
       "あなたんて大嫌い！", 
       "それもいいんだけどさあ、もうちょっと安いものはないの？",
       "先輩が大好きです！大好き！",
       "ウンコって汚い！キモイ！絶対嫌！",
        "先輩！一緒にご飯食べに行きませんか？ 先輩大好き！先輩大好き！先輩大好き！先輩大好き！",
        """こんにちは。
○○部の山田花子です。

突然のお手紙、驚かせてしまってすみません。
直接気持ちを伝える勇気がなくて…
でもどうしても田中さんに気持ちを伝えたくてペンをとりました。

初めて出会ったのは新入社員歓迎会でした。
一目見た瞬間から「素敵な人だな」と思っていた私は
ずっと田中さんが気になっていました。

すると、お酒が飲めないのに周りからすすめられて、
どうしていいのかわからず困っていた私を田中さんがかばってくれましたね。

そのさりげない優しさが本当にうれしくて…
胸の奥がきゅんとなったのを覚えています。

あの日から無意識にいつも田中さんの姿を目で追うようになりました。
目が合っただけでドキドキしたり、
お話できた日は１日中幸せな気持ちだったり…
私の中で田中さんへの「好き」っていう気持ちがどんどん大きくなっていきました。

そして、今でも忘れられないのは去年の花火大会のこと。
２人っきりではなかったけど、私にとっては田中さんとの初めてのお出かけ。
何日も前から洋服を選んで、前の日はあまりの緊張でほとんど眠れませんでした。

当日は思った以上に人が多くて、私はみんなに付いていくのがやっと…
ふと周りを見ると、いつの間にかみんなとはぐれてしまって
「このまま会えなかったらどうしよう」と不安でいっぱいだった時、
人混みの中から田中さんが私を見つけてくれましたね。

ホッとして思わず涙が出そうになったけど
あの時、「よかった…」と微笑む田中さんを見ながら
ずっとそばにいたい…と強く思いました。

誰に対しても相手の目をまっすぐに見て話をする誠実なところも
常に冷静沈着なのに、時々子供みたいに無邪気に笑うところも大好きです。

田中さん、不器用で迷子になってしまうドジな私ですが、
よかったらお付き合いしてもらえませんか？

田中さん大好きです

お返事お待ちしてます。"""
    ]

    # https://github.com/Hironsan/asari
    for test_item in test_sentence:
        sonar = Sonar()
        result = sonar.ping(text=test_item)
        #print(result)
        print("negative={0} and positive={1}".format(result['classes'][0]['confidence'], result['classes'][1]['confidence']))
#
#    for test_item in test_sentence:
#        emotion = analyze_emotion(test_item)
#        print(emotion)
