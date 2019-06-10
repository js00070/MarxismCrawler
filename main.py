import requests
import json
from requests.utils import quote
import threading
import os
from retrying import retry
import argparse

import glob
import re

from reportlab.lib import utils
from reportlab.pdfgen import canvas

#----------------------------------------------------------------------
def sorted_nicely( l ):
    """ 
    # http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
 
    Sort the given iterable in the way that humans expect.
    """ 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#----------------------------------------------------------------------
def unite_pictures_into_pdf(outputPdfName, pathToSavePdfTo, pathToPictures, splitType, numberOfEntitiesInOnePdf, listWithImagesExtensions, picturesAreInRootFolder, nameOfPart):
    
    if numberOfEntitiesInOnePdf < 1:
        print("Wrong value of numberOfEntitiesInOnePdf.")
        return
    if len(listWithImagesExtensions) == 0:
        print("listWithImagesExtensions is empty.")
        return
    
    if picturesAreInRootFolder == False:
        foldersInsideFolderWithPictures = sorted_nicely(glob.glob(pathToPictures + "\\*\\"))
        # print(foldersInsideFolderWithPictures)
        if len(foldersInsideFolderWithPictures) != 0:
            picturesPathsForEachFolder = []
            for iFolder in foldersInsideFolderWithPictures:
                picturePathsInFolder = []
                for jExtension in listWithImagesExtensions:
                    picturePathsInFolder.extend(glob.glob(iFolder + "*." + jExtension))
                picturesPathsForEachFolder.append(sorted_nicely(picturePathsInFolder))
            if splitType == "folder":
                numberOfFoldersAdded = 0;
                for iFolder in picturesPathsForEachFolder:
                    if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) == 0:
                        endNumber = numberOfFoldersAdded + numberOfEntitiesInOnePdf
                        if endNumber > len(picturesPathsForEachFolder):
                            endNumber = len(picturesPathsForEachFolder)
                        filename = []
                        if numberOfEntitiesInOnePdf > 1:
                            filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfFoldersAdded + 1) + '-' + str(endNumber) + "_of_" + str(len(picturesPathsForEachFolder)) + ".pdf")
                        elif numberOfEntitiesInOnePdf == 1:
                            filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfFoldersAdded + 1) + "_of_" + str(len(picturesPathsForEachFolder)) + ".pdf")
                        c = canvas.Canvas(filename)
                    for jPicture in iFolder:
                        img = utils.ImageReader(jPicture)
                        imagesize = img.getSize()
                        c.setPageSize(imagesize)
                        c.drawImage(jPicture, 0, 0)
                        c.showPage()
                    numberOfFoldersAdded += 1
                    if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) == 0:
                        c.save()
                        print("created", filename)
                if (numberOfFoldersAdded % numberOfEntitiesInOnePdf) != 0:
                        c.save()
                        print("created", filename)
            elif splitType == "picture":
                numberOfPicturesAdded = 0;
                totalNumberOfPictures = 0;
                for iFolder in picturesPathsForEachFolder:
                    totalNumberOfPictures += len(iFolder)
                for iFolder in picturesPathsForEachFolder:
                    for jPicture in iFolder:
                        if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
                            endNumber = numberOfPicturesAdded + numberOfEntitiesInOnePdf
                            if endNumber > totalNumberOfPictures:
                                endNumber = totalNumberOfPictures
                            filename = []
                            if numberOfEntitiesInOnePdf > 1:
                                filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + '-' + str(endNumber) + "_of_" + str(totalNumberOfPictures) + ".pdf")
                            elif numberOfEntitiesInOnePdf == 1:
                                filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + "_of_" + str(totalNumberOfPictures) + ".pdf")
                            c = canvas.Canvas(filename)
                        img = utils.ImageReader(jPicture)
                        imagesize = img.getSize()
                        c.setPageSize(imagesize)
                        c.drawImage(jPicture, 0, 0)
                        c.showPage()
                        numberOfPicturesAdded += 1
                        if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
                            c.save()
                            print("created", filename)
                if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) != 0:
                        c.save()
                        print("created", filename)
            elif splitType == "none":
                filename = os.path.join(pathToSavePdfTo, outputPdfName + ".pdf")
                c = canvas.Canvas(filename)
                for iFolder in picturesPathsForEachFolder:
                    for jPicture in iFolder:
                        img = utils.ImageReader(jPicture)
                        imagesize = img.getSize()
                        c.setPageSize(imagesize)
                        c.drawImage(jPicture, 0, 0)
                        c.showPage()
                c.save()
                print("created", filename)
            else:
                print("Wrong splitType value")
        else:
            print("No pictures found.")
        return
        
    if picturesAreInRootFolder == True:
        picturesInsideFolderWithPictures = []
        for iExtension in listWithImagesExtensions:
            picturesInsideFolderWithPictures.extend(glob.glob(pathToPictures + "\\*." + iExtension))
        picturesInsideFolderWithPictures = sorted_nicely(picturesInsideFolderWithPictures)
        if len(picturesInsideFolderWithPictures) != 0:
            if splitType == "picture":
                numberOfPicturesAdded = 0
                totalNumberOfPictures = len(picturesInsideFolderWithPictures)
                for iPicture in picturesInsideFolderWithPictures:
                    if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
                        endNumber = numberOfPicturesAdded + numberOfEntitiesInOnePdf
                        if endNumber > totalNumberOfPictures:
                            endNumber = totalNumberOfPictures
                        filename = []
                        if numberOfEntitiesInOnePdf > 1:
                            filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + '-' + str(endNumber) + "_of_" + str(totalNumberOfPictures) + ".pdf")
                        elif numberOfEntitiesInOnePdf == 1:
                            filename = os.path.join(pathToSavePdfTo, outputPdfName + "_" + nameOfPart + "_" + str(numberOfPicturesAdded + 1) + "_of_" + str(totalNumberOfPictures) + ".pdf")
                        c = canvas.Canvas(filename)
                    img = utils.ImageReader(iPicture)
                    imagesize = img.getSize()
                    c.setPageSize(imagesize)
                    c.drawImage(iPicture, 0, 0)
                    c.showPage()
                    numberOfPicturesAdded += 1
                    if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) == 0:
                        c.save()
                        print("created", filename)
                if (numberOfPicturesAdded % numberOfEntitiesInOnePdf) != 0:
                    c.save()
                    print("created", filename)
            elif splitType == "none":
                filename = os.path.join(pathToSavePdfTo, outputPdfName + ".pdf")
                c = canvas.Canvas(filename)
                for iPicture in picturesInsideFolderWithPictures:
                    try:
                        img = utils.ImageReader(iPicture)
                        
                        imagesize = img.getSize()
                        c.setPageSize(imagesize)
                        c.drawImage(iPicture, 0, 0)
                        c.showPage()
                    except Exception as e:
                        print(e)
                c.save()
                print("created", filename)
            else:
                print("Wrong splitType value")
        else:
            print("No pictures found.")
        return



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
    #print("getting ",bookid,page)
    url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=createEncryptFileUrl&bookid={}&page={}'
    response = requests.get(url.format(bookid,page), headers = h)
    #print(response.json())
    return response.json().get('result',{'imgurl': 'undefine'}).get('imgurl')

@retry
def getImgBuf(bookid: str, page: int) -> bytearray :
    imgurl = getImgUrl(bookid,page)
    #print(imgurl)
    url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=ReadImg&imgurl={}'.format(quote(imgurl))
    #print("imgurl:",url)
    #url = 'http://data.lilun.cn/Service/?logic=PDFReaderController&call=ReadImg&imgurl=Ql8wMTAyMDEyMF8wMDEoMSkuanBn'
    response = requests.get(url, headers = h)
    #print(response.content)
    return response.content

def saveImgAs(imgBuf: bytearray, filename: str):
    with open(filename,"wb") as fb:
        #print("saving img",filename)
        fb.write(imgBuf)
        fb.close()

def getBook(bookid: str) -> dict:
    print('========正在爬取{}========'.format(bookid))
    if not os.path.exists(bookid):
        os.makedirs(bookid)
    for page in range(1,1000):
        try:
            if os.path.exists("{}/{}.jpg".format(bookid,str(page).zfill(3))):
                print('第{}页已存在'.format(page))
                continue
            imgBuf = getImgBuf(bookid,page)
            if len(imgBuf) == 0:
                print("break out!")
                break
            print('下载第{}页'.format(page))
            saveImgAs(imgBuf,"{}/{}.jpg".format(bookid,str(page).zfill(3)))
        except Exception as e:
            print(e)
            return {'status': False,'bookid': bookid,'failedAt': page}
    return {'status': True, 'bookid': bookid}

def convert_to_pdf(bookid: str):
    print('========开始合成pdf========')
    outputPdfName = "{}".format(bookid)
    pathToSavePdfTo = "."
    pathToPictures = "{}".format(bookid)
    splitType = "none"
    numberOfEntitiesInOnePdf = 1
    listWithImagesExtensions = ["jpg"]
    picturesAreInRootFolder = True
    nameOfPart = "volume"
    unite_pictures_into_pdf(outputPdfName, pathToSavePdfTo, pathToPictures, splitType, numberOfEntitiesInOnePdf, listWithImagesExtensions, picturesAreInRootFolder, nameOfPart)
    print('pdf合成完毕！')

if __name__ == "__main__":
    # bookidgen = lambda n: 'B_01018{}_001'.format(136 + n) # 列宁全集 第 n 卷
    # # bookid = 'B_01018865_001' # 马克思主义政治经济学人物谱系
    # for n in range(3,60):
    #     getBook(bookidgen(n)) 
    '''
    bookid=B_01019144_001
    bookid=B_01019282_001
    bookid=B_01019283_001
    '''
    parser = argparse.ArgumentParser(description='输入若干bookid，从中国共产党思想理论资源数据库 http://data.lilun.cn/ 爬取马克思主义电子书籍')
    parser.add_argument('booklist', type=str, nargs='+',
                        help='bookid的列表')
    args = parser.parse_args()
    print('bookid的列表为：',args.booklist)
    resultlist = map(getBook,args.booklist)
    for res in resultlist:
        if res['status']:
            print('爬取{}成功！'.format(res['bookid']))
            convert_to_pdf(res['bookid'])
        else:
            print('爬取{}的第{}页时出错！中断爬取'.format(res['bookid'],res['failedAt']))
    



