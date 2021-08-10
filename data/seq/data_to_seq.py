import tensorflow
assert tensorflow.__version__ == "1.15"
import src.tokenizationK 
import src.seq as seq

def main():
    seq_in = []
    seq_out = []

    tokenizer = src.tokenizationK.FullTokenizer(vocab_file = "data\seq\resources\vocab.korean.rawtext.list")

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
    


if __name__ == "__main__":
    main()
