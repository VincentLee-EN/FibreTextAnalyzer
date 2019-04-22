# -*- encoding:utf-8 -*-
from __future__ import print_function
import json

from summary import TextRank4Keyword, TextRank4Sentence


def summary_text(file_name, text, segmenter, result_file):
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    file_name = file_name.replace('.', '_')
    tr4w = TextRank4Keyword.TextRank4Keyword(segmenter)
    tr4w.analyze(text=text, lower=True, window=2)

    result[file_name] = dict()
    result[file_name]['text'] = text.replace("\t", " ").replace("\n", " ")

    result[file_name]['summary_result'] = dict()
    result[file_name]['summary_result']['keywords'] = dict()
    for item in tr4w.get_keywords(10, word_min_len=2):
        result[file_name]['summary_result']['keywords'][item.word] = item.weight
        # print(item.word, item.weight)

    result[file_name]['summary_result']['keyphrase'] = list()
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        result[file_name]['summary_result']['keyphrase'].append(phrase)
        # print(phrase)

    tr4s = TextRank4Sentence.TextRank4Sentence(segmenter=segmenter)
    tr4s.analyze(text=text, lower=True, source='all_filters')

    result[file_name]['summary_result']['summary'] = list()
    for item in tr4s.get_key_sentences(num=3):
        result[file_name]['summary_result']['summary'].append((item.index, item.weight, item.sentence))
        # print(item.index, item.weight, item.sentence)

    # result[file_name]['word_list'] = tr4w.get_cws()
    result[file_name]['lexical_result'] = tr4w.get_lexical_res()

    json_str = json.dumps(result, ensure_ascii=False, indent=4)
    with open(result_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def summary_type(type_list, segmenter, result_file):
    base_dir = 'E:/python/Fibre_NLP/result/2019-4-15_2019-4-21/'

    with open(base_dir+result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)

    type_dict= dict()
    report = dict()
    report['keywords'] = dict()
    for item in type_list:
        type_dict[item] = ''

    for key, item in result.items():
        label = item['label'].split(',')[0]
        type_dict[label] += item['text']

    for type, text in type_dict.items():
        tr4w = TextRank4Keyword.TextRank4Keyword(segmenter)
        tr4w.analyze(text=text, lower=True, window=2)

        report['keywords'][type] = dict()
        for item in tr4w.get_keywords(50, word_min_len=2):
            report['keywords'][type][item.word] = item.weight

    json_str = json.dumps(report, ensure_ascii=False, indent=4)
    with open(base_dir + 'integrate_summary.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
