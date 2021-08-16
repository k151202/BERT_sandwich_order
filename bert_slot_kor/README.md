# 버트 미세조정 - 슬롯 태깅

1. pretrained BERT 모델을 모듈로 export

   - ETRI에서 사전훈련한 BERT의 체크포인트를 가지고 BERT 모듈을 만드는 과정.
   - `python export_korbert/bert_to_module.py -i {체크포인트 디렉토리} -o {output 디렉토리}`
   - 예시: `python export_korbert/bert_to_module.py -i /content/drive/MyDrive/004_bert_eojeol_tensorflow -o /content/drive/MyDrive/bert-module`

2. 데이터 준비

   - 모델을 훈련하기 위해 필요한 seq.in, seq.out이라는 2가지 파일을 만드는 과정.
   - 슬롯을 설정(/sandwich; /bread; 등)하고, 문장틀을 만든다.
   - 문장틀을 만든 후 코드를 통해 여러 문장들을 만든 후 data.txt에 저장한다.
   - seq.py의 Seq 클래스를 통해 슬롯내용을 검출하고 seq_in.txt, seq_out.txt를 만든다.
   - split.py의 Spliter 클래스를 이용하여 seq_in과 seq_out을 train, test, validation set으로 8:1:1의 비율로 나누어 각각의 텍스트 파일에 담는다.

3. Fine-tuing 훈련

   - argpaser를 이용해 인자값을 받을 수 있는 인스턴스 생성 후 입력받을 인자값을 등록한다.
   - 인자값(training set, validation set의 경로, 훈련된 모델을 저장할 경로, epoch 수, 배치사이즈)
   - 입력받은 인자값은 args에 저장된다.
   - 예시)
   - `python3 train.py -t /data/seq/resources/seq_in_train.txt -v /data/seq/resources/seq_in_valid.txt -s /saved_model_path -e 50 -bs 10`

4. 모델 평가

   - 훈련된 모델과 데이터의 경로를 입력해서 모델을 평가한다.
   - 예시)
   - `python3 eval.py -m /load_folder_path -d /data_folder_path`
   - 테스트의 결과는 --model에 넣어준 모델 경로 아래의 `test_results`에 저장된다.

5. Inference (임의의 문장을 모델에 넣어보기)

   - `python inference.py --model {훈련된 모델이 저장된 경로}`
   - 예시: `python inference.py --model saved_model/`
   - 모델 자체가 용량이 커서 불러오는 데까지 시간이 걸림
   - "Enter your sentence:"라는 문구가 나오면 모델에 넣어보고 싶은 문장을 넣어 주면 됨
   - quit라는 입력을 넣어 주면 종료

## Check List

eval.py

- [ ] 경로 고치기
- [x] test set 데이터 불러오기

inference.py

- [x] 필요한 모듈 불러오기
- [ ] 경로 고치기
- [x] 모델과 기타 필요한 것들 불러오기
- [x] 사용자가 입력한 한 문장을 슬롯태깅 모델에 넣어서 결과 뽑아내기

train.py

- [ ] 경로 고치기
- [x] validation data 불러오기
- [x] train set과 validation set을 둘 다 넣어서 model.fit 하기

utils.py

- [x] seq.in과 seq.out을 읽어들여서 리스트로 만들기

models/bert_slot_model.py

- [x] y_slots를 이용하여 slots_score를 만들기
- [ ] history_dict에 기록된 loss 변화 추이를 이미지로 저장하는 함수 만들기
