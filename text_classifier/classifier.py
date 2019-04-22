import codecs

import fastText.FastText as fasttext
from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter, pair
from Lexical_analyzer.dict.dict_util import segment_with_dict
from Lexical_analyzer.preprocess.text_preprocessing import text_preprocess


def predict(text,  segmenter):
    text = text.replace('\r', '').replace('\n', '').replace('\t', '')
    classifier = fasttext.load_model('E:/python/Fibre_NLP/text_classifier/model/try_5000.model')  # 加载模型

    result = segmenter.cws(text)
    return classifier.predict(result)  # 输出该文本的预测结果


def predict_type(text, cf):
    res = cf.predict(text)
    print(res)
    return res  # 输出该文本的预测结果


if __name__ == '__main__':
    segmenter = BiLSTMSegmenter(data_path='E:/python/Fibre_NLP/Lexical_analyzer/data/your_dict.pkl',
                                model_path='E:/python/Fibre_NLP/Lexical_analyzer/checkpoints/cws.ckpt/')
    classifier = fasttext.load_model('./try_5000.model')  # 加载模型
    text = codecs.open('./test_doc/affair_01.txt', 'r', 'utf-8').read()

    # 按文本分类
    # text = text_preprocess(text)
    # text = text.replace('\r','').replace('\n','').replace('\t','')
    # predict(text, segmenter)

    # 按段落分类
    text = text_preprocess(text)
    text = text.replace('\r','').replace('\t','').split('\n')
    for line in text:
        predict(line, classifier, segmenter)
