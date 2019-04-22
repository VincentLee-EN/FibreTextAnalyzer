# -*- encoding:utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter
import codecs
import os

from Lexical_analyzer.dict.dict_util import segment_with_dict
from . import util


def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')


class WordSegmentation(object):
    """ 分词 """

    def __init__(self, segmenter, stop_words_file=None, allow_speech_tags=util.allow_speech_tags):
        """
        Keyword arguments:
        stop_words_file    -- 保存停止词的文件路径，utf8编码，每行一个停止词。若不是str类型，则使用默认的停止词
        allow_speech_tags  -- 词性列表，用于过滤
        """

        allow_speech_tags = [util.as_text(item) for item in allow_speech_tags]
        self.segmenter = segmenter
        self.default_speech_tag_filter = allow_speech_tags
        self.stop_words = set()
        self.stop_words_file = get_default_stop_words_file()
        if type(stop_words_file) is str:
            self.stop_words_file = stop_words_file
        for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
            self.stop_words.add(word.strip())

    def segment(self, text, lower=True):
        """对一段文本进行分词，返回list类型的分词结果

        Keyword arguments:
        lower                  -- 是否将单词小写（针对英文）
        use_stop_words         -- 若为True，则利用停止词集合来过滤（去掉停止词）
        use_speech_tags_filter -- 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。    
        """
        text = util.as_text(text)
        lexical_result = self.segmenter.cut(text)
        segment_with_dict(text, lexical_result)

        word_list = list()
        word_list_stopwordfilter = list()
        word_list_speechtagfilter = list()
        for w in lexical_result:
            word = w.word.strip()
            if lower:
                word = word.lower()
            word_list.append(word)
            if word not in self.stop_words:
                word_list_stopwordfilter.append(word)
                if w.flag in self.default_speech_tag_filter:
                    word_list_speechtagfilter.append(word)

        return {'lexical_result': lexical_result, 'word_list': word_list,
                'word_list_stopwordfilter': word_list_stopwordfilter,
                'word_list_speechtagfilter': word_list_speechtagfilter}

    def segment_sentences(self, sentences, lower=True):
        """将列表sequences中的每个元素/句子转换为由单词构成的列表。

        sequences -- 列表，每个元素是一个句子（字符串类型）
        """

        res = {'lexical_result': [], 'words_no_filter': [], 'words_no_stop_words': [], 'words_all_filters': []}
        for sentence in sentences:
            sentence_res = self.segment(text=sentence, lower=lower)
            res['lexical_result'].append(sentence_res['lexical_result'])
            res['words_no_filter'].append(sentence_res['word_list'])
            res['words_no_stop_words'].append(sentence_res['word_list_stopwordfilter'])
            res['words_all_filters'].append(sentence_res['word_list_speechtagfilter'])

        return res


class SentenceSegmentation(object):
    """ 分句 """

    def __init__(self, delimiters=util.sentence_delimiters):
        """
        Keyword arguments:
        delimiters -- 可迭代对象，用来拆分句子
        """
        self.delimiters = set([util.as_text(item) for item in delimiters])

    def segment(self, text):
        res = [util.as_text(text)]

        util.debug(res)
        util.debug(self.delimiters)

        for sep in self.delimiters:
            text, res = res, []
            for seq in text:
                res += seq.split(sep)
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res


class Segmentation(object):

    def __init__(self, segmenter,
                 stop_words_file=None,
                 allow_speech_tags=util.allow_speech_tags,
                 delimiters=util.sentence_delimiters):
        """
        Keyword arguments:
        stop_words_file -- 停止词文件
        delimiters      -- 用来拆分句子的符号集合
        """
        self.ws = WordSegmentation(segmenter=segmenter, stop_words_file=stop_words_file,
                                   allow_speech_tags=allow_speech_tags)
        self.ss = SentenceSegmentation(delimiters=delimiters)

    def segment(self, text, lower=False):
        text = util.as_text(text)
        sentences = self.ss.segment(text)
        words = self.ws.segment_sentences(sentences=sentences, lower=lower)

        return util.AttrDict(
            sentences=sentences,
            lexical_result=words['lexical_result'],
            words_no_filter=words['words_no_filter'],
            words_no_stop_words=words['words_no_stop_words'],
            words_all_filters=words['words_all_filters']
        )


if __name__ == '__main__':
    pass
