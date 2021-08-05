import pandas as pd
import numpy as np
import random
import sys

##메뉴
#길이
length=['15cm','30cm','15센치','30센치','15센티','30센티']

#샌드위치
sandwich=['페퍼로니 피자썹', '이탈리안 비엠티', '에그마요', '스테이크 치즈',
          '써브웨이 클럽','로티세리 바비큐 치킨','햄', '참치', '미트볼',
          '풀드 포그 바비큐','치킨 데리야끼', '스파이시 이탈리안','쉬림프'
          ,'베지', '터키','비엘티','페퍼 치킨 슈니첼','K-바비큐', '터키 베이컨 아보카도','로스트 치킨']

#빵
bread=['화이트', '하티', '파마산 오레가노', '위트', '허니오트', '플랫']

#치즈
cheese=['아메리칸 치즈', '슈레드 치즈', '모짜렐라 치즈']

#추가토핑
add_topping=['미트', '쉬림프 더블업', '에그마요', '오믈렛',
             '아보카도', '베이컨','페퍼로니','치즈']

#야채제거
vegtable=['양상추 ','토마토','오이','피망','피클','올리브','할라피뇨','양파']

#소스
sauce=['랜치','마요네즈','스위트 어니언','허니 머스타드','스위트 칠리',
       '핫 칠리','사우스 웨스트 치폴레','머스타드','홀스래디쉬',
       '올리브 오일','레드와인 식초','소금','후추','스모크 바베큐']

#기타 문장 추가
list_ect = [
    #영업시간 관련사항
          '영업시간은 언제부터 언제까지 인가요?',
          '지금 주문 가능한가요?',
    #질의응답 관련사항
          '그냥 채팅으로 주문하면 되는건가요?',
    #배달,방문포장 관련
          '배달요금이 따로 있나요',
          '배달 가능한가요?',
          '방문포장 가능한가요?',
          '배달 가능 지역이 어디까지 인가요?',
    #메뉴 추천
          '메뉴가 너무 많은데 추천 해주세요',
          '메뉴 추천 해주세요',
    #불만사항 예상답변: 죄송합니다 저희매장에서 더욱 신경쓰도록 하겠습니다.
          '여기 알바생이 불친절 하던데 클레임은 어떻게 걸까요',
          '음식이 너무 짜요',
          '왜 이렇게 오래 걸리나요?',
          '아 몰라 사장 나오라고 그래',
    #시간 안내
          '나오는데 얼마나 걸릴까요?',
          '배고픈데 빨리 해주세요',
    #기타
          '노래 좀 불러줘',
          '오 맛있어요 다음에도 주문 할 게요',
    #주문취소 및 변경
          '주문 취소 가능할까요?',
          '혹시 주문 취소 하려는데 괜찮을까요?',
          '오이 빼달라는걸 잊어서 오이 지금이라도 뺄 수 있을까요?',
          '아 맞다 제가 오이를 못먹어서 오이도좀 빼주세요',
           ]


# 접목어
leng =['','길이','길이는']
sand =['','고기','고기는']
brea =['','빵','빵은']
chee =['','치즈','치즈는']
sauc =['','소스','소스는']
together = ['','이랑','랑','하고']
cont = ['','으로', '로']
con = ['','주시고', '해주시고', '하고','해주세요', '부탁드립니다', '해주십시오', '주십시오', '할게요']
finish = ['','해주세요.', '부탁드립니다.', '해주십시오.', '주십시오.', '할게요.', '주세요.', '해줘요.']
exclude = ['빼고']
vege = ['','채소','야채']
top = ['','토핑은','추가토핑은','추가 토핑은']


#순서섞기 리스트 저장
s_l = f'{random.choice(leng)} /length;{random.choice(length)}/ {random.choice(cont)} '
s_s = f'{random.choice(sand)} /sandwich;{random.choice(sandwich)}/ {random.choice(cont)} '
s_b = f'{random.choice(brea)} /bread;{random.choice(bread)}/ {random.choice(cont)} '
s_ch = f'{random.choice(chee)} /cheese;{random.choice(cheese)}/ {random.choice(cont)} '
s_ev = f'{random.choice(vege)} /vegetable;{random.choice(vegtable)}/ {random.choice(exclude)} '
s_sa = f'{random.choice(sauc)} /sauce;{random.choice(sauce)}/ {random.choice(cont)} '
lists=[s_l,s_s,s_b,s_ch,s_ev,s_sa]


#사용 함수들
#중복 난수 제거
def Random_eliminate():
    exlist = []                               
    for i in range(0,5):
        a = random.randint(0,5)       
        while a in exlist :
            a = random.randint(0,5)
        exlist.append(a)
    return exlist

#2d to 1d
def flatten(input):
    flat = []
    for i in input:
        for j in i:
            flat.append(j)
    return flat


#순서 재정렬 및 누적저장
data = []
def gen_data() :
    for i in range(1,2001):
        temp = [Random_eliminate()]
        ttemp = flatten(temp)
        tttemp = lists[ttemp[0]]+f'{random.choice(con)} '+lists[ttemp[1]]+f'{random.choice(con)} '+lists[ttemp[2]]+f'{random.choice(con)} '+lists[ttemp[3]]+f'{random.choice(con)} '+lists[ttemp[4]]+f'{random.choice(finish)}'
        data.append(tttemp)
        if i ==2000:
            for j in range(0,len(list_ect)):
                data.append(list_ect[j])
    return data
