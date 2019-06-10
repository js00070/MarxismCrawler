import json
import requests
import os
import time

archiveMap = {
    '习近平新时代中国特色社会主义思想库': {'id':769,'size':185},
    '马克思主义著作库': {'id':313,'size':1834},
    '党和国家主要领导人著作库': {'id':314,'size':778},
    '党和国家重要文献库': 315,
    '经典著作选编和重要论述摘编库': 327,
    '党的思想理论研究成果库': 415,
    '中国特色社会主义建设库': 416,
    '法律法规库': 419,
    '中共党史库': 422,
    '党的建设库': 423,
    '革命时期出版图书库': {'id': 424, 'size': 1651},
    '国际共运资料库': {'id': 425, 'size': 575},
    '历史知识库': {'id': 426, 'size': 3836},
    '哲学知识库': {'id':427, 'size': 1716},
}

def getBookInfo(archiveID: int, size: int) -> list:
    response = requests.post(url='http://data.lilun.cn/Service/?logic=bookController&call=getBookByColumn',
                  data='specialid={}&columnId={}&page=0&pageSize={}'.format(archiveID,archiveID,size),
                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
    bookInfoList = json.loads(response.content).get('result').get('bookinfo',[])
    return bookInfoList

if __name__ == "__main__":
    bookInfoList = []
    bookInfoList.extend(getBookInfo(archiveMap['国际共运资料库']['id'],archiveMap['国际共运资料库']['size']))
    bookInfoList.extend(getBookInfo(archiveMap['哲学知识库']['id'],archiveMap['哲学知识库']['size']))
    bookInfoList.extend(getBookInfo(archiveMap['历史知识库']['id'],archiveMap['历史知识库']['size']))
    bookInfoList.extend(getBookInfo(archiveMap['马克思主义著作库']['id'],archiveMap['马克思主义著作库']['size']))
    with open('bookid.csv','a',encoding='utf-8') as fp:
        for info in bookInfoList:
            record = '{},{},{},{},{},{}\n'.format(info.get('isbn','unknown'),info['bookid'],info['bookname'],info.get('author','unknown'),info.get('publish','unknown'),info.get('releaseDate','unknown'))
            fp.write(record)
        fp.close()