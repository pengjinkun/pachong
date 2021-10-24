import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
# import xlwt
import numpy as np
import re
import jieba
from wordcloud import WordCloud
import imageio


# 获得城市本地宝的主界面
def getCityHref(cityname):
    # 获得主界面
    url = 'http://m.bendibao.com/city.php'
    page = requests.get(url=url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    page.encoding = 'gbk2312'
    soup = BeautifulSoup(page.text,'lxml')
    # 获得所有城市的超链接
    all_city_href = soup.find_all('div',attrs={'class':'col-xs-4 col-sm-3 col-md-2 col-lg-1'})
    for city in all_city_href[12:]:
        if city.get_text()==cityname:
            return city.a.get('href')


# 获得搜索栏链接
def getSearchHref(cityHref):
    page_son = requests.get(url=cityHref,headers={'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'},verify=False)
    page_son.encoding = 'gbk2312'
    soup_son = BeautifulSoup(page_son.text, "html.parser")
    soup_son = soup_son.select(".search")
    return soup_son[0].get('href')


# 获得政策的链接
def getPolicyHref(policy,searchHref):
    query_url = searchHref.split('?')[0]+'?q='+policy+'&click=1&'+searchHref.split('?')[1]+'&nsid='
    page_search_result = requests.get(url=query_url,headers={'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'},verify=False)                
    soup_search_result = BeautifulSoup(page_search_result.text, "html.parser")
    policyHref = {'href1':soup_search_result.select('.c-title')[0].a.get('href'),
    'href2':soup_search_result.select('.c-title')[1].a.get('href')}
    return policyHref


# 处理政策的内容
def dealPolicy(dic):
    policy1 = dic['href1']
    policy2 = dic['href2']
    response1 = requests.get(url=policy1,headers={'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    response2 = requests.get(url=policy2,headers={'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    response1.encoding = 'gbk2312'
    response2.encoding = 'gbk2312'

    txt1 = BeautifulSoup(response1.text,"html.parser")
    txt2 = BeautifulSoup(response2.text,"html.parser")

    try:
        div_content1 = txt1.find_all('div',attrs={"id":"bo"})
        p_content1 = div_content1[0].find_all('p')
        for p in p_content1:
            with open('政策.txt','a',encoding="utf-8") as f:   
                f.write(p.get_text()+'\n')    
    except:
        print("政策1error")
  

    try:
        div_content2 = txt2.find_all('div',attrs={"id":"bo"})
        p_content2 = div_content2[0].find_all('p')
        for p in p_content2:
            with open('政策.txt','w',encoding="utf-8") as f:   
                f.write(p.get_text())   
    except:
          print("政策2error")
    
             



def getPolicyInformation(cityname,policy):
    cityHref = getCityHref(cityname)
    searchHref = getSearchHref(cityHref)
    dic = getPolicyHref(policy,searchHref)
    dealPolicy(dic)



# def read_deal_text():
#     with open("政策.txt","r",encoding='utf-8') as f:
#         txt=f.read()
#     re_move=["，","。"," ",'\n','\xa0']
#        #去除无效数据
#     for i in re_move:
#         txt=txt.replace(i," ") 
#     word=jieba.lcut(txt)  #使用精确分词模式
 
    
#     with open("txt_save.txt",'w') as file:
#         for i in word:    
#             file.write(str(i)+' ')
#     print("文本处理完成")
 
# def img_grearte():
#     mask=imageio.imread("D:\\pythonProject\\机器学习\爬虫\\top250\\80pzqeih.png")
#     with open("txt_save.txt","r") as file:
#         txt=file.read()
#     word=WordCloud(background_color="white",\
#                     width=800,\
#                    height=800,
#                    font_path='simhei.ttf',
#                    mask=mask,
#                    ).generate(txt)
#     word.to_file('test.png')
#     print("词云图片已保存")
    
    # plt.imshow(word)    #使用plt库显示图片
    # plt.axis("off")
    # plt.show()
 

if __name__=='__main__':
    getPolicyInformation()
    # read_deal_text()
    # img_grearte()


