# -*- coding: utf-8 -*-

import sys
import re
import argparse

def remove_brackets(sentences, delimiter=" "):

    sentences_without_brackets = []
    pattern = r"[\(\[].+?[\]\)]|\{\{.+?\}\}"
    for sen in sentences:
        sen = sen.replace("（", "(").replace("）", ")") + " " + delimiter
        for m in re.findall(pattern, sen):
            sen = sen.replace(m, "") # remove string including brackets
        sentences_without_brackets.append(sen)

    return sentences_without_brackets

def split_line(line, delimiter):
    pattern = r"「.+?」"
    for m in re.findall(pattern, line):
        tmp_m = m.replace(delimiter, "")
        line = line.replace(m, tmp_m)

    return line.split(delimiter)[:-1]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--vocab-limit", type=int, dest="vocab_limit", default=0, help="vocabulary limit to filterout")
    parser.add_argument("--word-limit", type=int, dest="word_limit", default=100000000, help="word limit")
    args = parser.parse_args()

    delimiter = "。"

    dic = {}
    num_words_count = 0 
    with open("sentences.tmp", "w") as f:
        # 標準入力を一行ずつ読み込み
        for line in sys.stdin:

            b_sentences = split_line(line, delimiter) # before
            a_sentences = remove_brackets(b_sentences, delimiter=delimiter) # after

            for a in a_sentences:
                if len(a) > 40 and len(a) < 800:
                    words = a.split()
                    num_words_count += len(words) # 単語数をカウント
                    for w in words:
                        dic[w] = dic.get(w, 0) + 1
                    f.write(a + "\n")

            if num_words_count > args.word_limit:
                break


    vocab_dict = {}
    with open("sentences.tmp", "r") as f:
        for sen in f:
            print " ".join([w if dic[w] > args.vocab_limit else "<unk>" for w in sen.strip().split()])
            """
            for w in sen.strip().split():
                if dic[w] > args.vocab_limit:
                    vocab_dict[w] = vocab_dict.get(w, 0) + 1
                else:
                    vocab_dict["<unk>"] = vocab_dict.get("<unk>", 0) + 1
            """

    #print "# of words:", num_words_count
    #print "# of vocab:", len(dic)
    #print "# of vocab(reduced):", len(vocab_dict)

if __name__ == '__main__':
    main()
