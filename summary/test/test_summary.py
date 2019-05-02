# -*- encoding:utf-8 -*-
from __future__ import print_function

import codecs
import json

from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter
from summary import TextRank4Keyword, TextRank4Sentence


def summary(text, segmenter, result_file):
    tr4w = TextRank4Keyword.TextRank4Keyword(segmenter)
    tr4w.analyze(text=text, lower=True, window=2)
    result = dict()

    result['keywords'] = dict()
    for item in tr4w.get_keywords(10, word_min_len=1):
        result['keywords'][item.word] = item.weight
        print(item.word, item.weight)

    result['keyphrase'] = list()
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        result['keyphrase'].append(phrase)
        print(phrase)

    tr4s = TextRank4Sentence.TextRank4Sentence(segmenter=segmenter)
    tr4s.analyze(text=text, lower=True, source='all_filters')

    result['summary'] = list()
    for item in tr4s.get_key_sentences(num=3):
        result['summary'].append((item.index, item.weight, item.sentence))
        print(item.index, item.weight, item.sentence)

    json_str = json.dumps(result, ensure_ascii=False, indent=4)
    with open(result_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

    return tr4w.get_cws()

if __name__ == '__main__':
    segmenter = BiLSTMSegmenter(data_path='../../Lexical_analyzer/data/your_dict.pkl',
                                model_path='../../Lexical_analyzer/checkpoints/cws.ckpt/')
    text = codecs.open('../test_doc/2019032601.txt', 'r', 'utf-8').read()
    # cws_result = segmenter.cut(text)
    # for item in cws_result:
    #     print(item.word + '/' + item.flag, end='  ')
    tr4w = TextRank4Keyword.TextRank4Keyword(segmenter)

    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    cws_result = tr4w.get_cws()

    result = dict()

    print('关键词：')
    result['keywords'] = dict()
    for item in tr4w.get_keywords(10, word_min_len=2):
        result['keywords'][item.word] = item.weight
        print(item.word, item.weight)

    print()
    print('关键短语：')
    result['keyphrase'] = list()
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        result['keyphrase'].append(phrase)
        print(phrase)

    tr4s = TextRank4Sentence.TextRank4Sentence(segmenter=segmenter)
    tr4s.analyze(text=text, lower=True, source='all_filters')

    print()
    print('摘要：')
    result['summary'] = list()

    for item in tr4s.get_key_sentences(num=3):
        result['summary'].append((item.index, item.weight, item.sentence))
        print(item.index, item.weight, item.sentence)

    json_str = json.dumps(result, ensure_ascii=False, indent=4)
    with open('E:/python/Fibre_NLP/summary/result/2019032601_summary.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

