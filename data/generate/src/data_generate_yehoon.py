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

from itertools import combinations
from itertools import permutations
import pandas as pd
import random

# 슬롯의 종류
keys = ['sandwich','length','cheese','bread','vegetable','sauce']
kor_keys = ['샌드위치','길이','치즈','빵','채소','소스']

# 슬롯이 담을 수 있는 내용을 슬롯 이름에 맞게 튜플로 변수 생성 
for key, kor_key in zip(keys,kor_keys):
    exec("%s = tuple(pd.read_csv('../resources/%s.csv'))"%(key,kor_key))

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

## 빵과 샌드위치를 고르는 문장
pre_oven_data = []

# 빵과 샌드위치 (겹문장 앞부분)
pre_oven_bread_sandwich = []

for bread in menu['bread']:
    for sandwich in menu['sandwich']:
        predicate = '으로 주세요.'
        if has_coda(bread):
            # 받침 없는 경우
            predicate = '로 주세요.'
        order = '/sandwich;'+sandwich+'/에 '

        # "{샌드위치}에 {무엇}(으)로 주세요."
        pre_oven_data.append(order+'/bread;'+bread+'/'+predicate)

        # "{샌드위치}에 빵은 {무엇}(으)로 주세요."
        pre_oven_data.append(order+'빵은 /bread;'+bread+'/'+predicate)
        
        # "{빵}에 {샌드위치}(으)로 주세요."
        predicate = '으로 주세요.'
        if has_coda(sandwich):
            # 받침 없는 경우
            predicate = '로 주세요.'
        order = '/bread;'+bread+'/에 '+'/sandwich;'+sandwich+'/'+predicate
        pre_oven_data.append(order)

        # "{빵}에 {샌드위치}(으)로 해주시고, "
        pre_oven_bread_sandwich.append(order[:-5]+' 해주시고, ')

# 빵과 메뉴가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data,200):
    sentences.append(sentence)

## 빵과 길이
pre_oven_data = []

for bread in menu['bread']:
    for length in menu['length']:
        # {길이} {빵} 순서
        predicate = '으로 해주세요.'
        if has_coda(bread):
            # 받침 없는 경우
            predicate = '로 해주세요.'
        order = '/length;'+length+'/ '+'/bread;'+bread+'/'+predicate

        # "빵은 {길이} {빵}(으)로 해주세요."
        pre_oven_data.append('빵은 '+order)

        # "{길이} {빵}(으)로 해주세요."
        pre_oven_data.append(order)
        
        # {빵} {길이} 순서
        predicate = '으로 해주세요.'
        if has_coda(length):
            # 받침 없는 경우
            predicate = '로 해주세요.'
        order = '/bread;'+bread+'/ '+'/length;'+length+'/'+predicate

        # "빵은 {빵} {길이}으로 해주세요."
        pre_oven_data.append('빵은 '+order)

        # "{빵} {길이}으로 해주세요."
        pre_oven_data.append(order)
  
# 빵과 길이가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data,200):
    sentences.append(sentence)

## 빵, 길이, 샌드위치
pre_oven_data = []         

for bread in menu['bread']:
    bread = '/bread;'+bread+'/'
    for length in menu['length']:
        length = '/length;'+length+'/'
        # 빵 종류 또는 빵 종류와 길이 
        bread_infos = [bread, bread+' '+length, length+' '+bread]
        for bread_info in bread_infos:
            for sandwich in menu['sandwich']:
                ### "{무엇}에다가 {무엇}으로 주세요."
                # (빵)(+길이), (샌드위치)
                predicate = '으로 주세요.'
                if has_coda(sandwich):
                    # 받침이 없으면
                    predicate = '로 주세요.'
                sandwich = '/sandwich;'+sandwich+'/'

                pre_oven_data.append(bread_info+'에다가 '+sandwich+predicate)

                   
# 빵, 길이, 샌드위치가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data,200):
    sentences.append(sentence)

pre_oven_data = []  

## 빵, 샌드위치, 치즈
for cheese in menu['cheese']:
    predicate = '으로 할게요.'
    if has_coda(cheese):
        # 받침 없는 경우
        predicate = '로 할게요.'
    order = '치즈는 '+'/cheese;'+cheese+'/'+predicate
    
    # "{빵}에 {샌드위치} 해주시고, 치즈는 {치즈}(으)로 할게요."
    for x in pre_oven_bread_sandwich:
        pre_oven_data.append(x+order)
  
# 빵, 샌드위치, 치즈가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data,200):
    sentences.append(sentence)

## 빵, 길이, 샌드위치, 치즈
pre_oven_data = []  

for cheese in menu['cheese']:
    predicate = '으로 할게요.'
    if has_coda(cheese):
        # 받침 없는 경우
        predicate = '로 할게요.'
    order = '치즈는 '+'/cheese;'+cheese+'/'+predicate

    # "{길이} {빵}에 {샌드위치} 해주시고, 치즈는 {치즈}로 할게요."
    for x in pre_oven_bread_sandwich:
         pre_oven_data.append('/length;'+random.choice(menu["length"])+'/ '+x+order) 
         
# 빵, 길이, 샌드위치, 치즈가 있는 문장 200개 추출 
for sentence in random.sample(pre_oven_data,200):
    sentences.append(sentence)

# 채소 슬롯이 여러 있는 문장
mult_veg_data = []

# 겹문장 채소 부분
post_oven_veg = []

# 연결어
connectives = ['이랑 ','하고 ',', ']

# 채소를 선택할 수 있는 최대 개수
MAX_VEGE = 4

veges = menu['vegetable']

for i in range(2,MAX_VEGE+1):
    # 채소 i 개 선택
    for p_veg in combinations(veges,i):
        # 채소 겹문장 부분
        order = ''
        for veg in p_veg:
            order+='/vegetable;'+veg+'/'+', '
        # "{채소} {채소} 빼주시고, "
        post_oven_veg.append(order[:-2] + ' 빼주시고, ')

        # 채소 홑문장
        for p_con in combinations(connectives,i-1):
            order = ''
            for veg,con in zip(p_veg[:-1],p_con):
                order+='/vegetable;'+veg+'/'
                if con == '이랑 ':
                    if has_coda(veg):
                        # 받침 없는 경우
                        con=con[1:]
                order+=con
            order+='/vegetable;'+p_veg[-1]+'/'

            # "{채소}(랑/하고/,) {채소}(랑/하고/,) {채소}(이)요."
            order2=order
            if not has_coda(p_veg[-1]):
                # 받침 없는 경우
                order2+='이'
            mult_veg_data.append(order2+'요.')

            # "{채소}(랑/하고/,) {채소}(랑/하고/,) {채소} 빼주세요."
            order+=' 빼주세요.'
            mult_veg_data.append(order)

            # "{veg}는 {채소}(랑/하고/,) {채소}(랑/하고/,) {채소} 빼주세요."
            for veg in cat['vegetable']:
                mult_veg_data.append(veg+'는 '+order)

            # "{채소}(랑/하고/,) {채소} 빼주시고 {채소}도 빼주세요."   
            order = ''
            for veg,con in zip(p_veg[:-2],p_con):
                order+='/vegetable;'+veg+'/'
                if con == '이랑 ':
                    if has_coda(veg):
                        # 받침 없는 경우
                        con=con[1:]
                order+=con
            order+='/vegetable;'+p_veg[-2]+'/'+' 빼주시고 '
            order+='/vegetable;'+p_veg[-1]+'/'+'도 빼주세요.'
            
            # "{veg}는 {채소}(랑/하고/,) {채소} 빼주시고 {채소}도 빼주세요."
            mult_veg_data.append(order)
            for veg in cat['vegetable']:
                mult_veg_data.append(veg+'는 '+order)

         # "{채소}, {채소} 그리고 {채소}요."       
        order=''
        for veg in p_veg[:-2]:
            order+='/vegetable;'+veg+'/'+', '
        order+='/vegetable;'+p_veg[-2]+'/'+' 그리고 '
        order+='/vegetable;'+p_veg[-1]+'/'+'요.'
        
        mult_veg_data.append(order)
                     
# 채소가 여러개 있는 문장 200개 추출 
for sentence in random.sample(mult_veg_data, 200):
    sentences.append(sentence)

# 소스가 여러개 있는 문장
mult_sauce_data = []
# 겹문장 소스 부분
post_oven_sauce = []
# 연결어
connectives = ['이랑 ','하고 ',', ']
# 긍정 서술어
pos_predicates = ['으로 해주세요.','으로 할게요.','으로 주세요.','으로 주이소.']
# 최대 소스 개수
MAX_SAUCE = 3

sauces = menu['sauce']
for i in range(2,MAX_SAUCE+1):
    # 소스 i 개 선택
    for p_sauces in combinations(sauces,i):
        # "{소스} {소스} 넣어주세요."
        order = ''
        for sauce in p_sauces:
            order+='/sauce;'+sauce+'/'+', '
        post_oven_sauce.append(order[:-2] + ' 넣어주세요.')
        
        # 소스 홑문장
        for p_con in combinations(connectives,i-1):
            order = ''
            for sauce,con in zip(p_sauces[:-1],p_con):
                order+='/sauce;'+sauce+'/'
                if con == '이랑 ':
                    if has_coda(sauce):
                        # 받침 없는 경우
                        con=con[1:]
                order+=con
            order+='/sauce;'+p_sauces[-1]+'/'
            # "{소스}(랑/하고/,) {소스}(랑/하고/,) {소스}(이)요."
            order2=order
            if not has_coda(p_sauces[-1]):
                # 받침 없는 경우
                order2+='이'
            mult_sauce_data.append(order2+'요.')
            
            # "{소스}(랑/하고/,) {소스}(랑/하고/,) {소스}(으)로 (긍정 서술어)."
            for pos_predicate in pos_predicates:
                if has_coda(p_sauces[-1]):
                    pos_predicate = pos_predicate[1:]
                mult_sauce_data.append(order+pos_predicate)

# 소스가 여러개 있는 문장 200개 추출 
for sentence in random.sample(mult_sauce_data, 200):
    sentences.append(sentence)

# 채소와 소스가 여러개 있는 문장 200개 추출
for x in random.sample(post_oven_sauce, 200):
    sentences.append(random.choice(post_oven_veg)+x)


## 완전 주문
# {빵} {길이} {샌드위치}에다가 치즈는 {치즈}로 해주시고, 채소는 {채소} 빼주시고,
# 소스는 {소스}로 해주세요.

# 주문 겹문장 앞 부분
complex_front = []
for bread in menu['bread']:
    bread = '/bread;'+bread+'/ '
    for length in menu['length']:
        length = '/length;'+length+'/ '
        for sandwich in menu['sandwich']:
            sandwich = '/sandwich;'+sandwich+'/'
            for cheese in menu['cheese']:
                cheese_predicate = '으로 해주시고, '
                if has_coda(cheese):
                    # 받침 없는 경우
                    cheese_predicate = '로 해주시고, '
                cheese = '/cheese;'+cheese+'/'
                complex_front.append(bread+length+sandwich+\
                                    '에다가 치즈는 '+cheese+\
                                   cheese_predicate)
# 채소 최대 개수                                   
MAX_VEG = 1
# 소스 최대 개수
MAX_SAUCE = 1
# 주문 겹문장 뒷 부분
complex_back = []
for i in range(1,MAX_VEG+1):
    for p_veg in permutations(menu['vegetable'],i):
        vegs = ''
        for veg in p_veg:
            vegs+='/vegetable;'+veg+'/ '
        for i in range(1,MAX_SAUCE+1):
            for p_sauce in permutations(menu['sauce'],i):
                sauces = ''
                for sauce in p_sauce:
                    sauces+='/sauce;'+sauce+'/ '
                sauce_predicate = '으로 해주세요.'
                if has_coda(sauce):
                    # 받침 없는 경우
                    sauce_predicate = '로 해주세요.'
                complex_back.append('채소는 '+\
                                   vegs+' 빼주시고, '+\
                                   sauces+sauce_predicate)

for _ in range(200):
    sentences.append(random.choice(complex_front)+random.choice(complex_back))

# 슬롯 없는 문장
no_slot_data = pd.read_table('../resources/no_slot_data.txt', sep='\n', header=None)

for sentence in no_slot_data:
    sentences.append(sentence)
    
return sentences
