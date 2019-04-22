import json
import pickle
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def dict_union(d1, d2):
    keys = d1.keys() | d2.keys()
    temp = {}
    for key in keys:
        temp[key] = sum([d.get(key, 0) for d in (d1, d2)])
    return temp


def get_week_keyword(json_file):
    with open(json_file, "r", encoding='utf-8') as f:
        return json.load(f)


def generate_keyword_cloud(week_keyword_dict, cloud_path):
    wc = WordCloud(
        background_color='white',  # 设置背景颜色
        font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=2000,  # 设置最大现实的字数
        stopwords=STOPWORDS,  # 设置停用词
        max_font_size=150,  # 设置字体最大值
        random_state=30  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.fit_words(week_keyword_dict)
    print('开始加载文本')
    # 改变字体颜色
    # 字体颜色为背景图片的颜色
    # wc.recolor(color_func='')
    # 显示词云图
    plt.imshow(wc)
    # 是否显示x轴、y轴下标
    plt.axis('off')
    # plt.show()
    # 获得模块所在的路径的
    d = path.dirname(__file__)
    print(d)
    # os.path.join()：  将多个路径组合后返回
    wc.to_file(path.join(d, cloud_path))
    print("生成词云成功")
