import os
from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter, pair
from Lexical_analyzer.dict.dict_util import segment_with_dict
from Lexical_analyzer.preprocess.text_preprocessing import text_preprocess

basedir = "E:/python/fibre_spider/" #这是我的文件地址，需跟据文件夹位置进行更改
dir_list = ['economy', 'market', 'product', 'tech']
##生成fastext的训练和测试数据集

ftrain = open("./corpus/FibreNews_1000_train.txt","w",encoding='utf-8')
ftest = open("./corpus/FibreNews_200_test.txt","w",encoding='utf-8')

segmenter = BiLSTMSegmenter(data_path='E:/python/Fibre_NLP/Lexical_analyzer/data/your_dict.pkl',
                                model_path='E:/python/Fibre_NLP/Lexical_analyzer/checkpoints/cws.ckpt/')

num = -1
for e in dir_list:
    num += 1
    indir = basedir + e + '/'
    files = os.listdir(indir)
    count = 0
    for fileName in files:
        count += 1
        filepath = indir + fileName
        with open(filepath,'r',encoding='utf-8') as fr:
            text = fr.read()
        text = text
        outline = segmenter.cws(text.replace("\t"," ").replace("\n"," "))
        outline = outline + "\t__label__" + e + "\n"
        # print(outline)
#         break
        print(count)
        if count <= 1000:
            ftrain.write(outline)
            ftrain.flush()
            continue
        elif count <= 1200:
            ftest.write(outline)
            ftest.flush()
            continue
        else:
            break

ftrain.close()
ftest.close()