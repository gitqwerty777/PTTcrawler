# encoding: utf-8
import sys
import json
import jieba
import jieba.analyse
import jieba.posseg

class DataParser:
    def __init__(self, jsonData):
        self.data = []
        for datum in jsonData:
            self.data.append(Data(datum))

    def printData(self):
        print self.data


class Data:
    def __init__(self, jsonDatum):
        #print str(jsonDatum).decode('unicode-escape').encode('utf-8')
        self.id = jsonDatum["a_ID"]
        self.author = jsonDatum["b_作者".decode('utf-8')]
        self.title = jsonDatum["c_標題".decode('utf-8')]
        self.date = jsonDatum["d_日期".decode('utf-8')]
        self.article = Article(jsonDatum["f_內文".decode('utf-8')])
        self.replies = []
        for jsonReply in jsonDatum["g_推文".decode('utf-8')]:
            self.replies.append(Reply(jsonReply))
        self.ip = jsonDatum["e_ip".decode('utf-8')]
        self.replyStat = jsonDatum["h_推文總數".decode('utf-8')]


class Reply:
    def __init__(self, jsonReply):
        self.type = jsonReply["狀態".decode('utf-8')]
        self.content = jsonReply["留言內容".decode('utf-8')]
        self.time = jsonReply["留言時間".decode('utf-8')]
        self.messager = jsonReply["留言者".decode('utf-8')]


class Article:
    def __init__(self, jsonArticle):
        '''

        seg_list = jieba.cut(jsonArticle, cut_all=False)
        print "/".join(seg_list)

        seg_list = jieba.cut_for_search(jsonArticle)
        print "-".join(seg_list)
        
        seg_list = jieba.analyse.extract_tags(jsonArticle, topK=20, withWeight=True)  # collect keywords based on TF-IDF
        for keyword in seg_list:
            print keyword[0], keyword[1]
        print "------------"

        seg_list = jieba.analyse.textrank(jsonArticle, topK=20, withWeight=True)  # collect keywords based on TF-IDF
        for keyword in seg_list:
            print keyword[0], keyword[1]
        print "------------"

        # Part of Speech
        words = jieba.posseg.cut(jsonArticle)
        for word, flag in words:
            if flag != 'x':
                print('(%s,%s)' % (word, flag))
        '''
        
        # print jsonArticle
        # segment
        # parse words


class ReplyStat:
    def __init__(self):
        pass
    

if __name__ == "__main__":
    fileName = sys.argv[1]
    
    with open(fileName) as data_file:
        data = json.load(data_file)
        dataParser = DataParser(data)

