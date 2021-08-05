from itertools import combinations
from itertools import permutations
import pandas as pd
import random

def gen_data():

    menu = get_menu()
    category = get_category()

    generator = Generator(200, menu, category)

    sentences = generator.generate()

    # 슬롯 없는 문장
    no_slot_data = pd.read_table('data/generate/resources/no_slot_data.txt', sep='\n', header=None)
    sentences.extend(list(no_slot_data[0]))

    return sentences

class Generator:
    def __init__(self, n:int, menu:dict, category:dict):
        #문장틀 당 생성할 문장 수 n
        self.n = n
        # 서브웨이 메뉴 menu
        self.menu = menu
        # 샌드위치 구성 항목 category
        self.category = category

    def generate(self):
        sentences = []
        sentences.extend(get_sample(self.gen_data_with_one(), self.n))
        sentences.extend(get_sample(self.gen_bread_sandwich(), self.n))
        sentences.extend(get_sample(self.gen_bread_length(), self.n))
        sentences.extend(get_sample(self.gen_bread_length_sandwich(), self.n))
        sentences.extend(get_sample(self.gen_bread_sandwich_cheese(), self.n))
        sentences.extend(get_sample(self.gen_pre_oven_data(), self.n))
        sentences.extend(get_sample(self.gen_mult_veg_data(), self.n))
        sentences.extend(get_sample(self.gen_mult_sauce_data(), self.n))
        sentences.extend(get_sample(self.gen_post_oven_data(), self.n))
        sentences.extend(get_sample(self.gen_complex_data(), self.n))
        
        return sentences

    def gen_data_with_one(self):
        # 슬롯이 하나인 문장 생성
        data_with_one = []
        # 긍정 서술어
        pos_predicates = ['으로 해주세요.','으로 할게요.','으로 주세요.','으로 주이소.']
        # 부정 서술어
        neg_predicate = ' 빼주세요.'
        # 일반 서술어
        predicate ='이요'

        for key,li in self.menu.items():
            for val in li:
                if key == 'vegetable':
                    # "{채소} 빼주세요."
                    data_with_one.append('/%s;%s/'%(key,val)+neg_predicate)

                    # "{veg}는 {채소} 빼주세요."
                    for veg in self.category[key]:
                        data_with_one.append(veg+'는'+'/%s;%s/'%(key,val)+neg_predicate)

                    # "{채소}은(는) 빼주세요."
                    postposition = fit("는",val)
                    data_with_one.append('/%s;%s/'%(key,val)+postposition+neg_predicate)
                    
                else:
                    for pos_predicate in pos_predicates:
                        # "{무엇}(으)로 해주세요/할게요/주세요."
                        pos_predicate = fit(pos_predicate,val)
                        data_with_one.append('/%s;%s/'%(key,val)+pos_predicate)

                        # "{종류}은(는) {무엇}(으)로 해주세요/할게요/주세요."
                        for x in self.category[key]:
                            postposition = fit("는",x)
                            data_with_one.append(x+postposition+' /%s;%s/'%(key,val)+pos_predicate)

            # "{무엇}(이)요"
                data_with_one.append('/%s;%s/'%(key,val)+fit(predicate,val))

        return data_with_one

    def gen_bread_sandwich(self):
        ## 빵과 샌드위치를 고르는 문장
        bread_sandwich = []

        for bread in self.menu['bread']:
            for sandwich in self.menu['sandwich']:
                predicate = fit('으로 주세요.',bread)
                order = '/sandwich;'+sandwich+'/에 '

                # "{샌드위치}에 {무엇}(으)로 주세요."
                bread_sandwich.append(order+'/bread;'+bread+'/'+predicate)

                # "{샌드위치}에 빵은 {무엇}(으)로 주세요."
                bread_sandwich.append(order+'빵은 /bread;'+bread+'/'+predicate)
                
                # "{빵}에 {샌드위치}(으)로 주세요."
                predicate = fit('으로 주세요.',sandwich)
                bread_sandwich.append('/bread;'+bread+'/에 '+'/sandwich;'+sandwich+'/'+predicate)
        
        return bread_sandwich

    def gen_bread_length(self):
        ## 빵과 길이
        bread_length = []

        for bread in self.menu['bread']:
            for length in self.menu['length']:
                # {길이} {빵} 순서
                predicate = fit('으로 해주세요.',bread)
                order = '/length;'+length+'/ '+'/bread;'+bread+'/'+predicate

                # "빵은 {길이} {빵}(으)로 해주세요."
                bread_length.append('빵은 '+order)

                # "{길이} {빵}(으)로 해주세요."
                bread_length.append(order)
                
                # {빵} {길이} 순서
                predicate = fit('으로 해주세요.',length)
                order = '/bread;'+bread+'/ '+'/length;'+length+'/'+predicate

                # "빵은 {빵} {길이}으로 해주세요."
                bread_length.append('빵은 '+order)

                # "{빵} {길이}으로 해주세요."
                bread_length.append(order)
        
        return bread_length

    def gen_bread_length_sandwich(self):
        ## 빵, 길이, 샌드위치
        bread_length_sandwich = []         

        for bread in self.menu['bread']:
            bread = '/bread;'+bread+'/'
            for length in self.menu['length']:
                length = '/length;'+length+'/'
                # 빵 종류 또는 빵 종류와 길이 
                bread_infos = [bread, bread+' '+length, length+' '+bread]
                for bread_info in bread_infos:
                    for sandwich in self.menu['sandwich']:
                        ### "{무엇}에다가 {무엇}으로 주세요."
                        # (빵)(+길이), (샌드위치)
                        predicate = fit('으로 주세요.',sandwich)
                        sandwich = '/sandwich;'+sandwich+'/'

                        bread_length_sandwich.append(bread_info+'에다가 '+sandwich+predicate)

        return bread_length_sandwich

    def gen_pre_bread_sandwich(self):
        # 빵과 샌드위치 (겹문장 앞부분)
        pre_oven_bread_sandwich = []

        for bread in self.menu['bread']:
            for sandwich in self.menu['sandwich']:
                # "{빵}에 {샌드위치}(으)로 해주시고, "
                predicate = fit('으로 해주시고, ',sandwich)
                pre_oven_bread_sandwich.append('/bread;'+bread+'/에 '+'/sandwich;'+sandwich+'/'+predicate)
        
        return pre_oven_bread_sandwich

    def gen_bread_sandwich_cheese(self):
        bread_sandwich_cheese = []  

        ## 빵, 샌드위치, 치즈
        for cheese in self.menu['cheese']:
            order = '치즈는 '+'/cheese;'+cheese+'/'+fit('으로 할게요.',cheese)
            
            # "{빵}에 {샌드위치} 해주시고, 치즈는 {치즈}(으)로 할게요."
            for x in self.gen_pre_bread_sandwich():
                bread_sandwich_cheese.append(x+order)
        
        return bread_sandwich_cheese

    def gen_pre_oven_data(self):
        ## 빵, 길이, 샌드위치, 치즈
        pre_oven_data = []  

        for cheese in self.menu['cheese']:
            predicate = '으로 할게요.'
            order = '치즈는 '+'/cheese;'+cheese+'/'+fit('으로 할게요.',cheese)

            # "{길이} {빵}에 {샌드위치} 해주시고, 치즈는 {치즈}로 할게요."
            for x in self.gen_pre_bread_sandwich():
                pre_oven_data.append('/length;'+random.choice(self.menu["length"])+'/ '+x+order) 
    
        return pre_oven_data

    def gen_mult_veg_data(self):
        # 채소 슬롯이 여러 있는 문장
        mult_veg_data = []

        # 연결어
        connectives = ['이랑 ','하고 ',', ']

        # 채소를 선택할 수 있는 최대 개수
        MAX_VEGE = 4

        veges = self.menu['vegetable']

        for i in range(2,MAX_VEGE+1):
            # 채소 i 개 선택
            for p_veg in combinations(veges,i):
                # 채소 홑문장
                for p_con in combinations(connectives,i-1):
                    order = ''
                    for veg,con in zip(p_veg[:-1],p_con):
                        order+='/vegetable;'+veg+'/'
                        if con == '이랑 ':
                            con = fit(con, veg)
                        order+=con
                    order+='/vegetable;'+p_veg[-1]+'/'

                    # "{채소}(랑/하고/,) {채소}(랑/하고/,) {채소}(이)요."
                    mult_veg_data.append(order+fit('이요',p_veg[-1]))

                    # "{채소}(랑/하고/,) {채소}(랑/하고/,) {채소} 빼주세요."
                    order+=' 빼주세요.'
                    mult_veg_data.append(order)

                    # "{veg}는 {채소}(랑/하고/,) {채소}(랑/하고/,) {채소} 빼주세요."
                    for veg in self.category['vegetable']:
                        mult_veg_data.append(veg+'는 '+order)

                    # "{채소}(랑/하고/,) {채소} 빼주시고 {채소}도 빼주세요."   
                    order = ''
                    for veg,con in zip(p_veg[:-2],p_con):
                        order+='/vegetable;'+veg+'/'
                        if con == '이랑 ':
                            con = fit(con, veg)
                        order+=con
                    order+='/vegetable;'+p_veg[-2]+'/'+' 빼주시고 '
                    order+='/vegetable;'+p_veg[-1]+'/'+'도 빼주세요.'
                    
                    # "{veg}는 {채소}(랑/하고/,) {채소} 빼주시고 {채소}도 빼주세요."
                    mult_veg_data.append(order)
                    for veg in self.category['vegetable']:
                        mult_veg_data.append(veg+'는 '+order)

                # "{채소}, {채소} 그리고 {채소}요."       
                order=''
                for veg in p_veg[:-2]:
                    order+='/vegetable;'+veg+'/'+', '
                order+='/vegetable;'+p_veg[-2]+'/'+' 그리고 '
                order+='/vegetable;'+p_veg[-1]+'/'+'요.'
                
                mult_veg_data.append(order)

        return mult_veg_data

    def gen_post_oven_veg(self):
        # 겹문장 채소 부분
        post_oven_veg = []

        # 채소를 선택할 수 있는 최대 개수
        MAX_VEGE = 4

        veges = self.menu['vegetable']

        for i in range(2,MAX_VEGE+1):
            # 채소 i 개 선택
            for p_veg in combinations(veges,i):
                # 채소 겹문장 부분
                order = ''
                for veg in p_veg:
                    order+='/vegetable;'+veg+'/'+', '
                # "{채소} {채소} 빼주시고, "
                post_oven_veg.append(order[:-2] + ' 빼주시고, ')

        return post_oven_veg

    def gen_mult_sauce_data(self):
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

        sauces = self.menu['sauce']
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
                            con = fit(con,sauce)
                        order+=con
                    order+='/sauce;'+p_sauces[-1]+'/'
                    # "{소스}(랑/하고/,) {소스}(랑/하고/,) {소스}(이)요."
                    mult_sauce_data.append(order+fit('이요.',p_sauces[-1]))
                    
                    # "{소스}(랑/하고/,) {소스}(랑/하고/,) {소스}(으)로 (긍정 서술어)."
                    for pos_predicate in pos_predicates:
                        mult_sauce_data.append(order+fit(pos_predicate,p_sauces[-1]))

        return mult_sauce_data

    def gen_post_oven_data(self):
        # 채소와 소스가 있는 문장
        post_oven_sauce = []
        # 최대 소스 개수
        MAX_SAUCE = 3

        sauces = self.menu['sauce']
        for i in range(2,MAX_SAUCE+1):
            # 소스 i 개 선택
            for p_sauces in combinations(sauces,i):
                # "{소스} {소스} 넣어주세요."
                order = ''
                for sauce in p_sauces:
                    order+='/sauce;'+sauce+'/'
                post_oven_sauce.append(order + ' 넣어주세요.')

        post_oven_veg = self.gen_post_oven_veg()

        return [random.choice(post_oven_veg)+x for x in post_oven_sauce]   

    def gen_complex_data(self):
        ## 완전 주문
        # {빵} {길이} {샌드위치}에다가 치즈는 {치즈}로 해주시고,
        # 채소는 {채소} 빼주시고, 소스는 {소스}로 해주세요.

        # 주문 겹문장 앞 부분
        complex_front = []
        for bread in self.menu['bread']:
            bread = '/bread;'+bread+'/ '
            for length in self.menu['length']:
                length = '/length;'+length+'/ '
                for sandwich in self.menu['sandwich']:
                    sandwich = '/sandwich;'+sandwich+'/'
                    for cheese in self.menu['cheese']:
                        cheese = '/cheese;'+cheese+'/'
                        complex_front.append(bread+length+sandwich+\
                                            '에다가 치즈는 '+cheese+\
                                        fit('으로 해주시고, ',cheese))
        # 채소 최대 개수                                   
        MAX_VEG = 1
        # 소스 최대 개수
        MAX_SAUCE = 1
        # 주문 겹문장 뒷 부분
        complex_back = []
        for i in range(1,MAX_VEG+1):
            for p_veg in permutations(self.menu['vegetable'],i):
                vegs = ''
                for veg in p_veg:
                    vegs+='/vegetable;'+veg+'/ '
                for i in range(1,MAX_SAUCE+1):
                    for p_sauce in permutations(self.menu['sauce'],i):
                        sauces = ''
                        for sauce in p_sauce:
                            sauces+='/sauce;'+sauce+'/ '
                        complex_back.append('채소는 '+vegs+\
                                        ' 빼주시고, '+sauces+\
                                        fit('으로 해주세요.',sauce))

        return [x+random.choice(complex_back) for x in complex_front]
        
def get_sample(data, n):
    # data에서 n개의 문장 추출
    return [sentence for sentence in random.sample(data,n)]

def fit(postposition,word):
    # 단어 word에 맞는 형태로 조사 postposition 리턴
    if has_coda(word):
        # 받침 없는 경우
        if postposition[0] == "은":
            postposition = "는"+postposition[1:]
        else:
            postposition = postposition[1:]

    return postposition

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


# 슬롯의 종류
keys = ['sandwich','length','cheese','bread','vegetable','sauce']
kor_keys = ['샌드위치','길이','치즈','빵','채소','소스']

def get_menu():
    # 슬롯이 담을 수 있는 내용을 슬롯 이름에 맞게 튜플로 변수 생성 
    for key, kor_key in zip(keys,kor_keys):
        exec("%s = tuple(pd.read_csv('data/generate/resources/%s.csv'))"%(key,kor_key))

    # 슬롯의 이름을 key 값, 슬롯의 내용을 튜플로 value 값으로 가지는 menu 사전 생성
    menu = {}
    for key in keys:
        exec("menu['%s'] = %s"%(key,key))

    return menu

def get_category():
    # 슬롯의 이름을 key 값, 슬롯의 다양한 명칭들을 리스트로 value 값으로 가지는 cat 사전 생성
    cat = {key:[val] for key,val in zip(keys, kor_keys)}
    cat['length']+=['크기','사이즈']
    cat['vegetable'].append('야채')

    return cat
