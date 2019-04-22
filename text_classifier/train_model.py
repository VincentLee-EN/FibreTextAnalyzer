import fastText.FastText as fasttext


def train_model(train_file):
    classifier = fasttext.train_supervised(train_file)  # 训练
    classifier.save_model('try_mycws.model')  # 保存模型


def test_model(model_file, test_file):
    classifier = fasttext.load_model(model_file)  # 加载模型
    labels_right = []
    texts = []
    with open(test_file, encoding='UTF-8') as fr:
        for line in fr:
            line = line.rstrip()
            labels_right.append(line.split("\t")[1].replace("__label__", ""))
            texts.append(line.split("\t")[0])
    predict_result = classifier.predict(texts)
    labels_predict = predict_result[0]

    text_labels = list(set(labels_right))
    text_predict_labels = list(set(labels_predict))

    report_f = open('report.log', 'w', encoding='utf-8')
    print('text_predict_labels' + str(text_predict_labels), file=report_f)
    print('text_labels' + str(text_labels), file=report_f)

    A = dict.fromkeys(text_labels, 0)  # 预测正确的各个类的数目
    B = dict.fromkeys(text_labels, 0)  # 测试数据集中各个类的数目
    C = dict.fromkeys(text_predict_labels, 0)  # 预测结果中各个类的数目

    for i in range(0, len(labels_right)):
        B[labels_right[i]] += 1
        C[labels_predict[i]] += 1
        if '__label__' + labels_right[i] == labels_predict[i]:
            A[labels_right[i]] += 1

    print('预测正确的各个类的数目' + str(A), file=report_f)
    print('测试数据集中各个类的数目' + str(B), file=report_f)
    print('预测结果中各个类的数目' + str(C), file=report_f)
    # 计算准确率，召回率，F值
    for key in B:
        try:
            if '__label__' + key in C:
                r = float(A[key]) / float(B[key])
                p = float(A[key]) / float(C['__label__' + key])
                f = p * r * 2 / (p + r)
                print("%s:\t p:%f\t r:%f\t f:%f" % (key, p, r, f), file=report_f)
        except:
            print("error:", key, "right:", A.get(key, 0), "real:", B.get(key, 0), "predict:", C.get(key, 0),
                  file=report_f)


if __name__ == '__main__':
    # text = codecs.open('./test_doc/economy_01.txt', 'r', 'utf-8').read().replace('\r','').replace('\n','').replace('\t','')
    # predict(text)

    # train_model('./corpus/news_10000_train.txt')
    test_model('try_mycws.model', './corpus/news_10000_test.txt')
