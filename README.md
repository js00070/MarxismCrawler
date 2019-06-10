# MarxismCrawler
从中国共产党思想理论资源数据库 http://data.lilun.cn/ 爬取马克思主义电子书籍

# 安装依赖

python版本3.7

```python
pip install -r requirements.txt
```

# 使用示例

爬取bookid分别为B_01019144_001、B_01019282_001、B_01019283_001的三本书，会在当前目录创建三个文件夹，文件夹里是每一页的jpg图片

并且会在下载图片完毕后，自动在当前目录生成由jpg图片合成的pdf文档，pdf文档由bookid命名

```python
python main.py B_01019144_001 B_01019282_001 B_01019283_001
```

# 使用建议

## 获取bookid

打开 http://data.lilun.cn/ 首页，搜索想要的书籍，搜到后，点击“在线阅读”，页面会显示未登录状态，但网页URL中会有bookid信息，示例如下

```
http://data.lilun.cn/Service/?logic=PDFReaderController&call=readPDF&bookid=B_01018144_001&page=1&html=selectText_NOINC&from=online&searchChar=undefined
```

目前爬取了一部分书名与bookid的对应关系，保存在了bookid.csv中，有需要可自行检索或批量下载

