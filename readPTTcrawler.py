# encoding: utf-8
import sys
import json
from types import *
import jieba
import jieba.analyse
import jieba.posseg
from collections import *

# 38521 39182 4/18 5/..
# can't crawl page without title

class PTTDataParser:
    def __init__(self, jsonData):
        self.data = []
        for datum in jsonData:
            self.data.append(Data(datum))

    def analyze(self):
        # TODO: sort userlist and use binary search
        self.userList = []
        for datum in self.data:
            for reply in datum.replies:
                if reply.replier not in self.userList:
                    self.userList.append(reply.replier)

        userMatrix = [[] for i in range(len(self.userList))]
        articleMatrix = [[] for i in range(self.data[-1].id+1)]
        for datum in self.data:
            for reply in datum.replies:
                userIndex = self.userList.index(reply.replier)
                articleMatrix[datum.id].append(userIndex)
                userMatrix[userIndex].append(datum.id)

        exclusiveList = ["", "，".decode('utf-8'), "\n", "\t", "。".decode('utf-8'), "、".decode('utf-8'), "｜".decode('utf-8')]  # a lot of words...
        with open("multiMatrix.txt", "w") as data_file:
            for datum in self.data:
                seg_list = jieba.cut(datum.article.content, cut_all=False)
                termCounter = Counter()
                for segment in seg_list:
                    if segment in termCounter:
                        termCounter[segment] += 1
                    else:
                        termCounter[segment] = 1
                data_file.write("%d " % len(termCounter.most_common()))
                for term in exclusiveList:
                    del termCounter[term]
                for term, count in termCounter.most_common():
                    data_file.write("%s:%d " % (term.encode('utf-8'), count))
                data_file.write("\n")

        with open("userList.txt", "w") as data_file:
            for user in self.userList:
                data_file.write("%s\n" % user)

        with open("userMatrix.txt", "w") as data_file:
            for i, articleList in enumerate(userMatrix):
                data_file.write("%d " % len(articleList))
                for articleID in articleList:
                    data_file.write("%d " % articleID)
                data_file.write("\n")

        with open("articleMatrix.txt", "w") as data_file:
            for i, userList in enumerate(articleMatrix):
                data_file.write("%d " % len(userList))
                for userID in userList:
                    data_file.write("%d " % userID)
                data_file.write("\n")

    def printData(self):
        print "printdata"
        for datum in self.data:
            print datum


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
        self.replyStat = ReplyStat(jsonDatum["h_推文總數".decode('utf-8')])

    def __repr__(self):
        s = ""
        for i, item in enumerate([self.id, self.author, self.title, self.date, self.article, self.replies, self.ip, self.replyStat]):
            if type(item) == UnicodeType:
                s += str(item.encode("utf-8"))+"\n"
            elif type(item) == ListType:
                for element in item:
                    s += str(element) + "\n"
            else:
                s += str(item)+"\n"
        return s
                


class Reply:
    def __init__(self, jsonReply):
        self.type = jsonReply["狀態".decode('utf-8')]
        self.content = jsonReply["留言內容".decode('utf-8')]
        self.time = jsonReply["留言時間".decode('utf-8')]
        self.replier = jsonReply["留言者".decode('utf-8')]

    def __repr__(self):
        return ("%s %s: %s %s" % (self.type, self.replier, self.content, self.time)).encode('utf-8')


class Article:
    def __init__(self, jsonArticle):
        self.content = jsonArticle

        
        '''
        # tokenization
        seg_list = jieba.cut(jsonArticle, cut_all=False)
        print "/".join(seg_list)
        seg_list = jieba.cut_for_search(jsonArticle)
        print "-".join(seg_list)

        # collect keywords based on TF-IDF
        seg_list = jieba.analyse.extract_tags(jsonArticle, topK=20, withWeight=True)
        for keyword in seg_list:
            print keyword[0], keyword[1]
        print "------------"

        # collect keywords based on textrank
        seg_list = jieba.analyse.textrank(jsonArticle, topK=20, withWeight=True)
        for keyword in seg_list:
            print keyword[0], keyword[1]
        print "------------"

        # Part of Speech
        words = jieba.posseg.cut(jsonArticle)
        for word, flag in words:
            if flag != 'x':
                print('(%s,%s)' % (word, flag))

        # collect keywords based on textrank
        seg_list = jieba.analyse.textrank(jsonArticle, topK=20, withWeight=True)
        for keyword in seg_list:
            print keyword[0], keyword[1]
        print "------------"
        
        '''

    def __repr__(self):
        return self.content.encode("utf-8")


class ReplyStat:
    def __init__(self, jsonReplyStat):
        self.total = jsonReplyStat['all']
        self.good = jsonReplyStat['g']
        self.bad = jsonReplyStat['b']
        self.neutual = jsonReplyStat['n']

    def __repr__(self):
        return "推文 %d 噓文 %d 箭頭 %d 總計 %d" % (self.good, self.bad, self.neutual, self.total)
    

if __name__ == "__main__":
    fileName = sys.argv[1]

    with open(fileName) as data_file:
        data = json.load(data_file)
        dataParser = PTTDataParser(data)

    dataParser.analyze()
    # dataParser.printData()

