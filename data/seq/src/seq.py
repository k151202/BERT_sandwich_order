import re


# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def combine(word, jongsung):
  # word 마지막 글자에 jongsung을 받침으로 한 단어를 리턴
  if jongsung == 'ᆫ':
    jongsung = 'ㄴ'
  if jongsung == 'ᆼ':
    jongsung = 'ㅇ'
  if jongsung == '[UNK]':
    jongsung = 'ㅂ'
  if jongsung == 'ᆷ':
    jongsung = 'ㅁ'
  if jongsung == 'ᆯ':
    jongsung = 'ㄹ'
  return word[:-1]+chr(ord(word[-1])+JONGSUNG_LIST.index(jongsung))


class Seq:
  def __init__(self, data, tokenizer):
    # 토크나이징할 문장
    self.data = self.prep(data)

    # seq.in 을 담는 리스트
    self.seq_in = []
    
    # seq.out 을 담는 리스트
    self.seq_out = []

    # 슬롯태깅이 안 된 data의 시작 index
    self.index = 0

    # data의 index에 슬롯
    self.is_slot = ""

    # data에서 찾지 못한 토큰
    self.unmatched_word = ""

    # 처리해야하는 공백
    self.has_space = False

    # 토크나이저
    self.tokenizer = tokenizer

  def prep(self, data):
    # "/",";" 이외의 특수문자 제거
    pat = re.compile("[^\w\s/;]")
    data = pat.sub("",data)

    # 슬롯 뒤에 띄어쓰기 추가
    pat = re.compile("/")
    data = pat.sub("/ ",data)

    # 이중공백을 공백으로 변환
    pat = re.compile("\s{2,}")
    data = pat.sub(" ",data)

    return data.lower()

  def get_seq_in(self):
    data = self.data

    # 태그 제거
    pat = re.compile("/\s\w+;")
    data = pat.sub("",data)

    # 특수문자 제거
    pat = re.compile("[^\w\s]")
    data = pat.sub("",data)

    # 토크나이즈
    data = self.tokenizer.tokenize(data)
    self.seq_in = data

    return data

  def get_seq_out(self):
    # 띄어쓰기를 "_"로 바꿈
    self.data = re.sub(" ","_",self.data)

    # seq_out 생성
    for token in self.seq_in:
      if self.index >= len(self.data):
        break
      self.seq_out.append(self.get_slot(token))

    return self.seq_out

  def get_slot(self, token):
    pat = re.compile(token)

    # 슬롯 안이라면, 슬롯이 끝나는지 확인
    if self.is_slot:
      self.slot_end()

    # 슬롯이 아니라면, 슬롯이 시작하는지 확인
    if not self.is_slot:
      self.slot_start()

    # 토큰으로 찾은 단어
    matched_word = self.find_match(token)

    # 찾은 단어의 길이만큼 이동
    self.index+=len(matched_word)

    if self.is_slot:
      # 슬롯 안이라면, 태그 리턴
      return self.is_slot
    return 0

  def slot_end(self):
    # data의 슬롯이 끝나는 지를 확인하고, index를 이동
    subsentence = self.data[self.index:]
    end_m = re.match("/",subsentence)

    if end_m:
      self.index+=1
      self.is_slot = ""
      if self.has_space:
        self.index+=1
        self.has_space = False

  def slot_start(self):
    # data의 슬롯이 시작하는 지를 확인하고, index를 이동
    subsentence = self.data[self.index:]

    if subsentence[0]=='/':
      temp = re.match("/\w+;",subsentence).group()
      self.index+=len(temp)
      self.is_slot = temp[2:-1]

  def find_match(self,token):
    # data의 index부터의 문장에서 token 찾기
    matched_word = ""
    pat = re.compile(token)
    subsentence = self.data[self.index:]
    m = pat.match(subsentence)

    if m:
      matched_word = m.group()
    else:
      if token[-1] == "_":
        # 단어 뒤에 띄어쓰기가 같이 토크나이징된 경우
        matched_word = token[:-1]
        self.has_space = True
      else:
        # 토크나이징 시 종성이 분리되니 경우
        if not self.unmatched_word:
          # 종성이 빠진 단어 저장
          self.unmatched_word = token
        else:
          # 종성이 빠진 단어에 종성 추가
          matched_word = combine(self.unmatched_word,token)
          self.unmatched_word = ""
               
    return matched_word
