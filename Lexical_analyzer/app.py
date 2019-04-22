# encoding=UTF-8

from Lexical_analyzer.cws.segmenter import BiLSTMSegmenter, pair
from Lexical_analyzer.dict.dict_util import segment_with_dict
from Lexical_analyzer.preprocess.text_preprocessing import text_preprocess


if __name__ == '__main__':
    segmenter = BiLSTMSegmenter(data_path='E:/python/Fibre_NLP/Lexical_analyzer/data/your_dict.pkl',
                                model_path='E:/python/Fibre_NLP/Lexical_analyzer/checkpoints/cws.ckpt/')
    #    print('示例2：', segmenter.predict('我和林长开的通话记录'))
    texts = [
        # '长飞光纤光缆有限公司创建于1988年5月，由中国电信集团公司、荷兰德拉克通信科技公司、武汉长江通信集团股份有限公司共同'
        # '投资。公司总部位于武汉市东湖高新技术开发区关山二路四号，占地面积达十七万平方米，是当今中国产品规格'
        # '最齐备、生产技术最先进、生产规模最大的光纤光缆产品以及制造装备的研发和生产基地。 '
        # '长飞光纤光缆有限公司的光纤光缆产品及多种网络建设解决方案能够满足每一个行业用户的不同需求，'
        # '已广泛应用于中国电信、中国移动、中国联通等通信运营商，以及电力、广电、交通、教育、国防、航天、'
        # '化工、石油、医疗等行业领域，并远销美国、日本、韩国、台湾、东南亚、中东、非洲等50多个国家和地区。'
        # ,
        # 'C114讯 3月28日消息（水易）据LightWave报道，瞻博网络（Juniper）计划进入可插拔光收发器领域，此前包括'
        # 'Ciena和Infinera等设备商也进入了该市场领域。据了解，Juniper已经宣布初步计划，使用2016年收购Aurrion'
        # '带来的硅光子学专业知识，推出100G QSFP28和400G QSFP-DD光模块。'
        # ,
        '烽火受任数字中国产业发展联盟多个工作组主席职位'
        # ,
        # '长飞光纤光缆有限公司的光纤光缆产品及多种网络建设解决方案能够满足每一个行业用户的不同需求，'
        # ,
        # "2003年10月15日，杨利伟乘由长征二号F火箭运载的神舟五号飞船首次进入太空，"
        # "象征着中国太空事业向前迈进一大步，起到了里程碑的作用。"
    ]
    for text in texts:
        text = text_preprocess(text)
        print('======')
        print(text)

        result = segmenter.cut(text)

        segment_with_dict(text,result)

        for w in result:
            print(w.word + '/' + w.flag, end='  ')
        print()


