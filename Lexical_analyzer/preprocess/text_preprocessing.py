import re


def text_preprocess(text):
    not_cuts = ['，', '；', '、', '。', '？', '！', '\?', '!']
    for punc in not_cuts:
        text = re.sub(r' *{} *'.format(punc), "{}".format(punc), text)
    return text