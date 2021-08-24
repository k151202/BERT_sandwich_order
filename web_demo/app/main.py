# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from sklearn import metrics
import tensorflow as tf
import os, pickle, re, difflib
import sys

sys.path.append(os.path.join(os.getcwd(), "../bert_slot_kor"))
from to_array.bert_to_array import BERTToArray
from models.bert_slot_model import BertSlotModel
from to_array.tokenizationK import FullTokenizer

graph = tf.compat.v1.get_default_graph()

# 메뉴 및 선택지
sandwich = [
    "페퍼 치킨 슈니첼",
    "페퍼로니 피자 썹",
    "쉬림프",
    "로스트 치킨",
    "에그마요",
    "K 바비큐",
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
    "스테이크 앤 치즈",
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
    #"topping": "추가토핑",
}

dic = {k:globals()[k] for k in menu}

cmds = {
    "명령어" : [],
    "샌드위치": sandwich,
    "길이": length,
    "빵": bread,
    "치즈": cheese,
    "소스": sauce,
    "채소": vegetable,
    #"topping": "추가토핑",
}

cmds["명령어"] = [k for k in cmds]

# enable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
config = tf.compat.v1.ConfigProto(
    intra_op_parallelism_threads=1,
    inter_op_parallelism_threads=1,
    allow_soft_placement=True,
    device_count={"GPU": 0},
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
        "sandwich": [],
        "length": [],
        "bread": [],
        "cheese": [],
        "sauce": [],
        "vegetable": [],
        # "topping": None,
    }
    # 점수제한
    app.score_limit = 0.7

    # 변수
    app.ask_veg = False
    app.confirm_veg = False
    app.ask_oven = False
    app.oven = None

    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg").strip()  # 사용자가 입력한 문장

    if userText[0] == "!":
        try:
            li = cmds[userText[1:]]
            message = "<br />\n".join(li)
        except:
            message = "입력한 명령어가 존재하지 않습니다."
        
        return message

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
    slot_text = {k: "" for k in app.slot_dict}

    # 슬롯태깅 실시
    for i in range(0, len(inferred_tags[0])):
        if slots_score[0][i] >= app.score_limit:
            catch_slot(i, inferred_tags, text_arr, slot_text)
        else:
            print("something went wrong!")

    # 메뉴판의 이름과 일치하는지 검증
    for k in app.slot_dict:
        for x in dic[k]:
            x = x.lower().replace(" ", "\s*")
            m = re.search(x, slot_text[k])
            if m:
                app.slot_dict[k].append(m.group())

    print(app.slot_dict)
    # 슬롯이 채워지지 않았을때 체크
    # empty_slot -> 비어있는 메뉴의 리스트
    empty_slot = [menu[k] for k in app.slot_dict if not app.slot_dict[k]]

    # 채소 슬롯이 비었을 때
    if "제외할 채소" in empty_slot:
        message = veg_msg(app, userText)
    elif empty_slot:
        message = ", ".join(empty_slot) + "가 아직 선택되지 않았습니다."
    else:
        # 빈 슬롯이 없을때
        if not app.ask_oven:
            if userText.strip() == "예":
                message = "오븐에 데워드릴까요?(예/아니오)"
                app.ask_oven = True
            elif userText.strip() == "아니오":
                message = "알겠습니다. 다시 주문해주세요."
                # 재주문을 위해 슬롯 초기화
                init_app(app)
            else:
                message = check_order_msg(app, menu)
        else:
            if userText.strip() == "예":
                app.oven = True
            elif userText.strip() == "아니오":
                app.oven = False
            message = "감사합니다. 주문이 완료되었습니다!"
  
    return message

def catch_slot(i, inferred_tags, text_arr, slot_text):
    if not inferred_tags[0][i] == "0":
        word_piece = re.sub("_", " ", text_arr[i])
        if word_piece == 'ᆫ':
            word = slot_text[inferred_tags[0][i]]
            slot_text[inferred_tags[0][i]] = word[:-1]+chr(ord(word[-1])+4)
        else:
            if word_piece == "오" and inferred_tags[0][i] == "vegetable":
                slot_text[inferred_tags[0][i]] += "오이"
            else:
                slot_text[inferred_tags[0][i]] += word_piece

def check_order_msg(app, menu):
    order = []
    for k, v in app.slot_dict.items():
        try:
            if len(v) == 1:
                order.append(f"{menu[k]}: {v[0]}")
            else:
                order.append(f"{menu[k]}: {', '.join(v)}")
        except:
            order.append(f"{menu[k]}: {None}")
    order = "<br />\n".join(order)

    message = f"""
        주문 확인하겠습니다.<br />
        ===================<br />
        {order}
        ===================<br />
        이대로 주문 완료하시겠습니까? (예 or 아니오)
        """

    return message

def init_app(app):
    app.slot_dict = {
        "sandwich": [],
        "length": [],
        "bread": [],
        "cheese": [],
        "sauce": [],
        "vegetable": [],
    }
    app.ask_veg = False
    app.confirm_veg = False

def veg_msg(app, userText):
    if not app.ask_veg:
        message = "안 드시는 채소를 선택해주세요."
        app.ask_veg = True
    else:
        if not app.confirm_veg:
            message = "선택한 채소가 없습니다. 채소는 다 넣어드릴까요?\n(예/아니오)"
            app.confirm_veg = True
        else:
            if userText.strip() == "예":
                message = f"""
                    채소는 다 넣어드리겠습니다.<br />
                    {", ".join(empty_slot)} + "가 아직 선택되지 않았습니다.
                    """
            elif userText.strip() == "아니오":
                app.ask_veg = False
                app.confirm_veg = False
    return message
