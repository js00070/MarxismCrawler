import requests
import json
from requests.utils import quote
import threading
import os
from retrying import retry

h = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "bagid=undefined; isLogin=true; JSESSIONID=rj0vxa4cg5pc1utzs6xzfy1d1",
    "Host": "data.lilun.cn",
    "Referer": "http://data.lilun.cn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

@retry
def getImgUrl(bookid: str, page: int) -> str :
    print("getting ",bookid,page)
    url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=createEncryptFileUrl&bookid={}&page={}'
    response = requests.get(url.format(bookid,page), headers = h)
    #print(response.json())
    return response.json().get('result',{'imgurl': 'undefine'}).get('imgurl')

@retry
def getImgBuf(bookid: str, page: int) -> bytearray :
    imgurl = getImgUrl(bookid,page)
    #print(imgurl)
    url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=ReadImg&imgurl={}'.format(quote(imgurl))
    print("imgurl:",url)
    #url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=ReadImg&imgurl=Ql8wMTAyMDEyMF8wMDEoMSkuanBn'
    response = requests.get(url, headers = h)
    #print(response.content)
    return response.content

def saveImgAs(imgBuf: bytearray, filename: str):
    with open(filename,"wb") as fb:
        print("saving img",filename)
        fb.write(imgBuf)
        fb.close()

if __name__ == "__main__":
    bookidgen = lambda n: 'B_01018{}_001'.format(136 + n) # 列宁全集 第 n 卷
    # bookid = 'B_01018865_001' # 马克思主义政治经济学人物谱系
    for n in range(3,60):
        bookid = bookidgen(n)
        print("列宁全集第{}卷".format(n))
        if not os.path.exists(bookid):
            os.makedirs(bookid)
        for page in range(1,1000):
            try:
                imgBuf = getImgBuf(bookid,page)
                if len(imgBuf) == 0:
                    print("break out!")
                    break
                saveImgAs(imgBuf,"{}/{}.jpg".format(bookid,str(page).zfill(3)))
            except Exception as e:
                print(e)
            

