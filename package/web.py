# 数值计算
import numpy as np

# 绘图
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from imageio import imread

#网站解析
import requests, lxml
from bs4 import BeautifulSoup
import jieba

def GetComment(url):
    # GetComment 是一个用于提取评课社区某一门课下所有课评的函数
    # 输入这门课的 url ，以 list 形式返回这门课的所有课评，列表元素为字符串
    
    # 获取源码并解析
    html = requests.get(url)
    soup = BeautifulSoup(html.text,"lxml")

    # 提取课评内容
    rawcomments = soup.find_all(name='div',attrs={"class":"review-content"})
    comments = []
    for content in rawcomments:
        comments = comments + [content.get_text()]
    
    # 以列表形式返回一门课的课评，列表元素为字符串
    return comments

def CatchWords(comments):
    # 选取长度足够的评课
    worthycomments = []
    for chunk in comments:
        if len(chunk) >= 250:
            worthycomments = worthycomments + [chunk] 
    allcomments = ' \n '.join(worthycomments)
        
    # 分词
    seg_str=jieba.cut(allcomments, cut_all=False)
    liststr="/".join(seg_str)

    # 去除停用词
    stopwords_path="./stopwords.txt"
    f_stop=open(stopwords_path, encoding='utf8')
    f_stop_text=f_stop.read()
    f_stop.close()

    mywordlist=[]
    f_stop_seg_list=f_stop_text.split('\n')

    # 将f_stop_text以'\n'切割字符串，返回列表赋值给f_stop_seg_list
    # 使用for循环，将liststr以 '/' 分割后的元素，一个个放入myword中，如果myword在的f_stop_seg_list  中，且myword.strip()长度大于1，就将myword添加到列表mywordlist中
    # 此步是为去除停用词，将去除的停用词的元素放到新建的列表中
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list)and len(myword.strip())>1:
            mywordlist.append(myword)
    
    ss = ' '.join(mywordlist)
    return ss

def TheWordCloud(comments):
    
    # 提取关键词
    words = CatchWords(comments)
    
    #绘制云图
    bg="./USTC.jpg"
    imgbg=imread(bg)

    a=WordCloud(font_path="./font/simkai.ttf", background_color='white', width=1000, height=800,mask=imgbg,colormap="summer")
    
    a.generate(words)
    plt.imshow(a)
    plt.axis("off")
    plt.show()