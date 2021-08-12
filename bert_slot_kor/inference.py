# -*- coding: utf-8 -*-

import os
import pickle
import argparse

# 필요한 모듈 불러오기 
from to_array.bert_to_array import BERTToArray
from to_array.tokenizationK import FullTokenizer
from models.bert_slot_model import BertSlotModel

import tensorflow as tf


if __name__ == "__main__":
    # Reads command-line parameters
    parser = argparse.ArgumentParser("Evaluating the BERT NLU model")
    parser.add_argument("--model", "-m",
                        help="Path to BERT NLU model",
                        type=str,
                        required=True)
    
    args = parser.parse_args()
    load_folder_path = args.model
    

    # this line is to disable gpu
    os.environ["CUDA_VISIBLE_DEVICES"]="-1"

    config = tf.ConfigProto(intra_op_parallelism_threads=1,
                            inter_op_parallelism_threads=1,
                            allow_soft_placement=True,
                            device_count = {"CPU": 1})
    sess = tf.compat.v1.Session(config=config)

    ################################ TODO 경로 고치기 ##################
    bert_model_hub_path = "/content/drive/MyDrive/bert-module"
    ####################################################################

    # 모델과 기타 필요한 것들 불러오기
    
    vocab_file = os.path.join(bert_model_hub_path,
                              "assets/vocab.korean.rawtext.list")
    bert_to_array = BERTToArray(vocab_file)
    
    # loading models
    print("Loading models ...")
    if not os.path.exists(load_folder_path):
        print("Folder `%s` not exist" % load_folder_path)
    
    tags_to_array_path = os.path.join(load_folder_path, "tags_to_array.pkl")
    with open(tags_to_array_path, "rb") as handle:
        tags_to_array = pickle.load(handle)
        slots_num = len(tags_to_array.label_encoder.classes_)
        
    model = BertSlotModel.load(load_folder_path, sess)
    
    
    while True:
        print("\nEnter your sentence: ")
        try:
            input_text = input().strip()
        except:
            continue
            
        if input_text == "quit":
            break
    
    # 사용자가 입력한 한 문장을 슬롯태깅 모델에 넣어서 결과 뽑아내기
    ################# TODO vocab_file 경로 채우기 ###########################
    tokenizer = FullTokenizer(vocab_file="")
    ########################################################################
    text_arr = tokenizer.tokenize(input_text)

    input_ids, input_mask, segment_ids = bert_to_array.transform(text_arr)
    
    # predict slots
    inferred_tags, slots_score = model.predict_slots([input_ids,
                                                      input_mask,
                                                      segment_ids],
                                                     tags_to_array)

    # 예측된 슬롯 출력
    print(inferred_tags)

   
    tf.compat.v1.reset_default_graph()
    
