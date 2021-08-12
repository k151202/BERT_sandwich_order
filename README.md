# BERT_sandwich_order  

## 목차
 - [프로젝트 주제](#프로젝트-주제)  
 - [서비스 기획 목적](#서비스-기획-목적)
 - [프로젝트 구현 과정](#프로젝트-구현-과정)
 - [의존성](#의존성)
 - [실행 방법](#실행-방법)

## 프로젝트 주제 

- BERT 기반 슬롯태깅 모델을 이용해서 샌드위치 주문 챗봇을 구현하는 프로젝트입니다.  

## 서비스 기획 목적

 - 사회적약자(장애인, 노인, 아동 등)의 사용이 어려움  
     > 기존 키오스크 주문이 어려움을 해소하기 위함  
     > 원활한 서비스를 위해서 대화형 시나리오를 설계  
 - 사용자의 메시지 분석을 통해 주문 과정을 구현  


## 프로젝트 구현 과정

 1. 데이터 수집  
    - 실제 프랜차이즈 메뉴(서브웨이)의 프로세스 이용
    - 상황에 따른 예상 질문 패턴 작성  
 2. 데이터 전처리
    - ETRI에서 BPE 알고리즘을 이용해 만든 토크나이저로 seq.in 생성
    - seq.in의 각 토큰에 맞는 태그를 seq.out으로 생성
 3. 파인튜닝
    - KoBert의 파인튜닝 사용

## 의존성
`tensorflow == 1.15` 


## 실행 방법
### 1. 데이터 생성
`data/generate`에 `data_merge.py`를 실행하면, `data.txt`가 'data/seq/resources'에 생성됨.

### 2. 데이터 전처리
`data/seq`에 `data_to_seq.py`를 실행하면, `seq_in.txt`과 `seq_out.txt`가 'data/seq/resources'에 생성됨.

### 3. 파인튜닝
> 진
