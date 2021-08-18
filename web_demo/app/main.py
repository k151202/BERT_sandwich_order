# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from sklearn import metrics
import tensorflow as tf
import os, pickle, re, difflib
import sys

sys.path.append(os.path.join(os.getcwd(), "bert_slot_kor"))
from to_array.bert_to_array import BERTToArray
from models.bert_slot_model import BertSlotModel
from to_array.tokenizationK import FullTokenizer

print(os.getcwd())

graph = tf.compat.v1.get_default_graph()

# enable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
config = tf.ConfigProto(
    intra_op_parallelism_threads=1,
    inter_op_parallelism_threads=1,
    allow_soft_placement=True,
    device_count={"CPU": 1},
)
sess = tf.compat.v1.Session(config=config)

# pretrained model path - 로컬에서 실행시 따로 다운로드 받아야함
# bert_model_hub_path = os.path.join(os.getcwd(), "bert-module")
bert_model_hub_path = "/content/drive/MyDrive/bert-module"

# fine-tuned model path - 로컬에서 실행시 따로 다운로드 받아야함
# load_folder_path = os.path.join(os.getcwd(), "save")
load_folder_path = "/content/drive/MyDrive/save"

# tokenizer vocab file path
vocab_file = os.path.join(bert_model_hub_path, "assets/vocab.korean.rawtext.list")
bert_to_array = BERTToArray(vocab_file)

tags_to_array_path = os.path.join(load_folder_path, "tags_to_array.pkl")
with open(tags_to_array_path, "rb") as handle:
    tags_to_array = pickle.load(handle)
    slots_num = len(tags_to_array.label_encoder.classes_)

model = BertSlotModel.load(load_folder_path, sess)

tokenizer = FullTokenizer(vocab_file=vocab_file)

app = Flask(__name__)
# 코랩에서 실행 시
run_with_ngrok(app)
app.static_folder = "static"


@app.route("/")
def home():
    # 슬롯 사전 만들기
    app.slot_dict = {
        "sandwich": None,
        "length": None,
        "bread": None,
        "cheese": None,
        "sauce": None,
        "vegetable": None,
        "topping": None,
    }
    # 점수제한
    app.score_limit = 0.8

    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg").strip()  # 사용자가 입력한 문장

    # 사용자가 입력한 문장을 토큰화
    text_arr = tokenizer.tokenize(userText)
    input_ids, input_mask, segment_ids = bert_to_array.transform([" ".join(text_arr)])

    # 예측
    with graph.as_default():
        with sess.as_default():
            inferred_tags, slots_score = model.predict_slots(
                [input_ids, input_mask, segment_ids], tags_to_array
            )

    # 결과 체크
    print("text_arr:", text_arr)
    print("inferred_tags:", inferred_tags[0])
    print("slots_score:", slots_score[0])

    # 슬롯에 해당하는 텍스트를 담을 변수 설정
    sandwich_text = ""
    length_text = ""
    bread_text = ""
    cheese_text = ""
    sauce_text = ""
    vegetable_text = ""
    topping_text = ""

    # 메뉴 및 선택지
    sandwich = [
        "페퍼 치킨 슈니첼",
        "페퍼로니 피자 썹",
        "쉬림프",
        "로스트 치킨",
        "에그마요",
        "K-바비큐",
        "로티세리 바비큐 치킨",
        "풀드 포크 바비큐",
        "이탈리안 비엠티",
        "비엘티",
        "미트볼",
        "햄",
        "참치",
        "써브웨이 클럽",
        "터키",
        "베지",
        "스테이크 & 치즈",
        "터키 베이컨 아보카도",
        "스파이시 이탈리안",
        "치킨 데리야끼",
    ]
    bread = ["화이트", "하티", "파마산 오레가노", "위트", "허니오트", "플랫"]
    cheese = ["아메리칸", "슈레드", "모짜렐라"]
    topping = ["미트", "쉬림프 더블업", "에그마요", "오믈렛", "아보카도", "베이컨", "페퍼로니", "치즈"]
    vegetable = ["양상추", "토마토", "오이", "피망", "피클", "올리브", "할라피뇨", "양파"]
    sauce = [
        "랜치",
        "마요네즈",
        "스위트 어니언",
        "허니 머스타드",
        "스위트 칠리",
        "핫 칠리",
        "사우스 웨스트 치폴레",
        "머스타드",
        "홀스래디쉬",
        "올리브 오일",
        "레드와인 식초",
        "소금",
        "후추",
        "스모크 바베큐",
    ]
    length = ["15cm", "30cm"]

    # 메뉴분류
    menu = {
        "sandwich": "샌드위치",
        "length": "길이",
        "bread": "빵종류",
        "cheese": "치즈",
        "sauce": "소스",
        "vegetable": "제외할 채소",
        "topping": "추가토핑",
    }

    # 슬롯태깅 실시
    for i in range(0, len(inferred_tags[0])):
        if slots_score[0][i] >= app.score_limit:
            if inferred_tags[0][i] == "sandwich":
                sandwich_text += text_arr[i]
                app.slot_dict["sandwich"] = re.sub("_", "", sandwich_text)

            elif inferred_tags[0][i] == "length":
                length_text += text_arr[i]
                app.slot_dict["length"] = re.sub("_", "", length_text)

            elif inferred_tags[0][i] == "bread":
                bread_text += text_arr[i]
                app.slot_dict["bread"] = re.sub("_", "", bread_text)

            elif inferred_tags[0][i] == "cheese":
                cheese_text += text_arr[i]
                app.slot_dict["cheese"] = re.sub("_", "", cheese_text)

            elif inferred_tags[0][i] == "sauce":
                sauce_text += text_arr[i]
                app.slot_dict["sauce"] = re.sub("_", "", sauce_text)

            elif inferred_tags[0][i] == "vegetable":
                vegetable_text += text_arr[i]
                app.slot_dict["vegetable"] = re.sub("_", "", vegetable_text)

            elif inferred_tags[0][i] == "topping":
                topping_text += text_arr[i]
                app.slot_dict["topping"] = re.sub("_", "", topping_text)
        else:
            print("something went wrong!")

    print(app.slot_dict)

    for k, v in app.slot_dict.items():
        answer = difflib.get_close_matches(app.slot_dict[k], k)
        if answer:
            app.slot_dict[k] = answer[0]
        else:
            app.slot_dict[k] = None

    # 슬롯이 채워지지 않았을때 예외처리
    empty_slot = [menu[k] for k, v in app.slot_dict.items() if app.slot_dict[k] == None]
    if empty_slot:
        message = ", ".join(empty_slot) + "를 선택해주세요!"
    else:
        message = "감사합니다. 주문이 완료되었습니다."

    return message  # 챗봇이 이용자에게 하는 말을 return


###############################################################################
