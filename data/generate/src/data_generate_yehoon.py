def has_coda(word):
    # 받침이 있는 단어로 끝나면 false를 리턴, 아니면 true를 리턴
    if is_hangul(word):
        return (ord(word[-1]) - 44032) % 28 == 0
    return True

def is_hangul(word):
    # word가 한글이면 true를 리턴, 아니면 false를 리턴
    code = ord(word[-1])
    if 44032 <= code <= 55203:
        return True
    return False


import pandas as pd
import random

# 슬롯의 종류
keys = ['sandwich','length','cheese','bread','vegetable','sauce']
kor_keys = ['샌드위치','길이','치즈','빵','채소','소스']

# 슬롯이 담을 수 있는 내용을 슬롯 이름에 맞게 튜플로 변수 생성 
for key, kor_key in zip(keys,kor_keys):
    exec("%s = tuple(pd.read_csv('%s.csv'))"%(key,kor_key))

# 슬롯의 이름을 key 값, 슬롯의 내용을 튜플로 value 값으로 가지는 menu 사전 생성
menu = {}
for key in keys:
    exec("menu['%s'] = %s"%(key,key))

# 슬롯의 이름을 key 값, 슬롯의 다양한 명칭들을 리스트로 value 값으로 가지는 cat 사전 생성
cat = {key:[val] for key,val in zip(keys, kor_keys)}
cat['length']+=['크기','사이즈']
cat['vegetable'].append('야채')

# 생성된 문장을 저장할 리스트
sentences = []

# 슬롯이 하나인 문장 생성
data_with_one = []
# 긍정 서술어
pos_predicates = ['으로 해주세요.','으로 할게요.','으로 주세요.','으로 주이소.']
# 부정 서술어
neg_predicate = ' 빼주세요.'
# 일반 서술어
predicate ='이요'

for key,li in menu.items():
    for val in li:
        if key == 'vegetable':
            # "{채소} 빼주세요."
            data_with_one.append('/%s;%s/'%(key,val)+neg_predicate)

            # "{veg}는 {채소} 빼주세요."
            for veg in cat[key]:
                data_with_one.append(veg+'는'+'/%s;%s/'%(key,val)+neg_predicate)

            # "{채소}은(는) 빼주세요."
            if has_coda(val):
                # 받침 없는 경우
                data_with_one.append('/%s;%s/'%(key,val)+'는'+neg_predicate)
            else:
                # 받침 있는 경우
                data_with_one.append('/%s;%s/'%(key,val)+'은'+neg_predicate)
        else:
            for pos_predicate in pos_predicates:
                # "{무엇}(으)로 해주세요/할게요/주세요."
                if has_coda(val):
                    # 받침 없는 경우
                    pos_predicate = pos_predicate[1:]
                data_with_one.append('/%s;%s/'%(key,val)+pos_predicate)

                # "{종류}은(는) {무엇}(으)로 해주세요/할게요/주세요."
                for x in cat[key]:
                    if has_coda(x):
                        data_with_one.append(x+'는 '+'/%s;%s/'%(key,val)+pos_predicate)
                    else:
                        data_with_one.append(x+'은 '+'/%s;%s/'%(key,val)+pos_predicate)
       # "{무엇}(이)요"
        temp = predicate
        if has_coda(val):
            # 받침 없는 경우
            temp = predicate[1:]
        data_with_one.append('/%s;%s/'%(key,val)+temp)

# 슬롯이 하나인 문장 200개 추출 
for sentence in random.sample(data_with_one,200):
    sentences.append(sentence)

## 빵과 메뉴를 고르는 문장
pre_oven_data1 = []

# 빵과 메뉴 (곁문장 앞부분)
pre_oven_bread_sandwich = []

for bread in menu['bread']:
    for sandwich in menu['sandwich']:
        predicate = '으로 주세요.'
        if has_coda(bread):
            # 받침 없는 경우
            predicate = '로 주세요.'
        order = '/sandwich;'+sandwich+'/에 '

        # "{샌드위치}에 {무엇}(으)로 주세요."
        pre_oven_data1.append(order+'/bread;'+bread+'/'+predicate)

        # "{샌드위치}에 빵은 {무엇}(으)로 주세요."
        pre_oven_data1.append(order+'빵은 /bread;'+bread+'/'+predicate)
        
        # "{빵}에 {샌드위치}(으)로 주세요."
        predicate = '으로 주세요.'
        if has_coda(sandwich):
            # 받침 없는 경우
            predicate = '로 주세요.'
        order = '/bread;'+bread+'/에 '+'/sandwich;'+sandwich+'/'+predicate
        pre_oven_data1.append(order)

        # "{빵}에 {샌드위치}(으)로 해주시고, "
        pre_oven_bread_sandwich.append(order[:-5]+' 해주시고, ')

# 빵과 메뉴가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data1,200):
    sentences.append(sentence)

## 빵과 길이
pre_oven_data2 = []

for bread in menu['bread']:
    for length in menu['length']:
        # {길이} {빵} 순서
        predicate = '으로 해주세요.'
        if has_coda(bread):
            # 받침 없는 경우
            predicate = '로 해주세요.'
        order = '/length;'+length+'/ '+'/bread;'+bread+'/'+predicate

        # "빵은 {길이} {빵}(으)로 해주세요."
        pre_oven_data2.append('빵은 '+order)

        # "{길이} {빵}(으)로 해주세요."
        pre_oven_data2.append(order)
        
        # {빵} {길이} 순서
        predicate = '으로 해주세요.'
        if has_coda(length):
            # 받침 없는 경우
            predicate = '로 해주세요.'
        order = '/bread;'+bread+'/ '+'/length;'+length+'/'+predicate

        # "빵은 {빵} {길이}으로 해주세요."
        pre_oven_data2.append('빵은 '+order)

        # "{빵} {길이}으로 해주세요."
        pre_oven_data2.append(order)
  
# 빵과 길이가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data2,200):
    sentences.append(sentence)

