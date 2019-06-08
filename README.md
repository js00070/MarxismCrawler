# MarxismCrawler
从中国共产党思想理论资源数据库 http://data.lilun.cn/ 爬取马克思主义电子书籍

# 安装依赖

python版本3.7

```python
pip install -r requirements.txt
```

# 使用示例

爬取bookid分别为B_01019144_001、B_01019282_001、B_01019283_001的三本书，会在当前目录创建三个文件夹，文件夹里是每一页的jpg图片

```python
python main.py B_01019144_001 B_01019282_001 B_01019283_001
```

# 使用建议

爬取结束后可以将jpg转成pdf，推荐使用imagemagick，不过会占用大量内存，需要调高imagemagick的默认内存限制

转换方式如下

```bash
convert *.jpg output.pdf
```