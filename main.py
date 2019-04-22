# encoding=UTF-8
import json
import os
import fastText.FastText as fasttext

from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter, pair
from Lexical_analyzer.dict.dict_util import segment_with_dict
from Lexical_analyzer.preprocess.text_preprocessing import text_preprocess
from text_classifier import classifier
from summary import summary
from summary import keyword_cloud


def classify(result_file):
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    cf = fasttext.load_model('E:/python/Fibre_NLP/text_classifier/model/fibre_2400.model')
    for file in result.keys():
        type = classifier.predict_type(result[file]['lexical_result']['cws'], cf)
        result[file]['label'] = type[0][0].replace('__label__', '') + ', ' + str(type[1][0])

    json_str = json.dumps(result, ensure_ascii=False, indent=4)
    with open(result_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def summarize(file_name, text, segmenter, result_file):
    return summary.summary_text(file_name=file_name, text=text, segmenter=segmenter,
                                result_file=result_file)


def summary_dump2json(docs_dir, result_dir, segmenter):
    weeks = os.listdir(docs_dir)

    for week in weeks:
        if week == '2019-4-7_2019-4-14':
            continue
        week_docs_dir = docs_dir + week + '/'
        week_result_path = result_dir + 'every_summary' + '.json'

        json_str = json.dumps({}, ensure_ascii=False, indent=4)
        with open(week_result_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)

        files = os.listdir(week_docs_dir)
        for file_name in files:
            file_path = week_docs_dir + file_name
            with open(file_path, 'r', encoding='utf-8') as fr:
                text = fr.read()
            print('file: ' + file_name + '; summarizing...')
            summarize(file_name, text, segmenter, week_result_path)

        # summary.summary_type(docs, segmenter, week_result_path)


def keyword2cloud(json_file, cloud_path):
    week_kw = keyword_cloud.get_week_keyword(json_file)['keywords']
    type_list = ['economy_market', 'tech_product']
    for key in type_list:
        if len(week_kw[key]) > 0:
            keyword_cloud.generate_keyword_cloud(week_kw[key], cloud_path + key + '.png')


if __name__ == '__main__':
    docs_dir = 'E:/python/Fibre_NLP/docs/'
    result_dir = 'E:/python/Fibre_NLP/result/2019-4-15_2019-4-21/'

    segmenter = BiLSTMSegmenter(data_path='E:/python/Fibre_NLP/Lexical_analyzer/data/your_dict.pkl',
                                model_path='E:/python/Fibre_NLP/Lexical_analyzer/checkpoints/cws.ckpt/')

    summary_dump2json(docs_dir, result_dir, segmenter)
    classify(result_dir + 'every_summary.json')
    # type_list = ['economy_market', 'tech_product']
    # summary.summary_type(type_list, segmenter, 'every_summary.json')
    #
    # keyword2cloud('E:/python/Fibre_NLP/result/2019-4-15_2019-4-21/integrate_summary.json',
    #               'E:/python/Fibre_NLP/result/2019-4-15_2019-4-21/')
