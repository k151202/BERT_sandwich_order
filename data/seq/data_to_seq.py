import tensorflow
assert tensorflow.__version__ == "1.15"
import src.tokenizationK 
import src.seq as seq
import src.split
import pandas as pd

def main():
    seq_in = []
    seq_out = []

    # ETRI에서 받은 /004_bert_eojeol_tensorflow/ 에 vocab.korean.rawtext.list 사용
    tokenizer = src.tokenizationK.FullTokenizer(vocab_file = "vocab.korean.rawtext.list")

    with open("data/seq/resources/data.txt", "r", encoding="utf-8") as f:
        for sentence in f.readlines():
            s = seq.Seq(sentence, tokenizer)
            seq_in.append(s.get_seq_in())
            seq_out.append(s.get_seq_out())

    
    with open("data/seq/resources/seq_in.txt", "w", encoding="utf-8") as f:
        for line in seq_in:
            f.write(line+"\n")

    with open("data/seq/resources/seq_out.txt", "w", encoding="utf-8") as f:
        for line in seq_out:
            f.write(line+"\n")

    # 데이터 train, test, valid set 으로 나누기
    spliter = split.Spliter(pd.Series(seq_in), pd.Series(seq_out))
    spliter.split()
    
    X_train, y_train = spliter.get_train()
    with open("data/seq/resources/train_seq_in.txt", "w", encoding="utf-8") as f:
      for line in X_train:
        f.write(" ".join(list(map(str,line)))+"\n")

    with open("data/seq/resources/train_seq_out.txt", "w", encoding="utf-8") as f:
      for line in y_train:
        f.write(" ".join(list(map(str,line)))+"\n")

    X_test, y_test = spliter.get_test()
    with open("data/seq/resources/test_seq_in.txt", "w", encoding="utf-8") as f:
      for line in X_test:
        f.write(" ".join(list(map(str,line)))+"\n")

    with open("data/seq/resources/test_seq_out.txt", "w", encoding="utf-8") as f:
      for line in y_test:
        f.write(" ".join(list(map(str,line)))+"\n")

    X_valid, y_valid = spliter.get_valid()
    with open("data/seq/resources/valid_seq_in.txt", "w", encoding="utf-8") as f:
      for line in X_valid:
        f.write(" ".join(list(map(str,line)))+"\n")

    with open("data/seq/resources/valid_seq_out.txt", "w", encoding="utf-8") as f:
      for line in y_valid:
        f.write(" ".join(list(map(str,line)))+"\n")

if __name__ == "__main__":
    main()
