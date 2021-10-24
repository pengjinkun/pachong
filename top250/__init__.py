import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plot
import xlwt
import numpy as np
import jieba
import PIL
import collections 
import matplotlib
import re

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.weight'] = 'bold'

def getJop(key):
    position = []   # 职位
    area = []       # 地区
    salary = []     # 工资
    company = []    #公司
    currentPage = '&currentPage='
    url0="https://www.liepin.com/zhaopin/?key="+key
    for n in range(10):
        url = url0+currentPage+str(n)
        page = requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"})
        soup = BeautifulSoup(page.text,"lxml")
        soup = soup.find_all("div",attrs={'class':'job-card-pc-container seo-job-card-action-box'})
        for i in soup:
            x = i.find_all('div',attrs={'class':'job-title-box'})
            position_i = x[0].find_all('div',attrs={'class':'ellipsis-1'}) #职位
            area_i = x[0].find_all('span',attrs={'class':'ellipsis-1'})    #地区
            for po in position_i:
                position.append(po.get_text())
            for ar in area_i:
                area.append(ar.get_text())

            salary_i = i.select('.job-salary')
            for sa in salary_i:
                salary.append(sa.get_text())

            company_i = i.select('.company-name')
            for com in company_i:
                company.append(com.get_text())

    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet(key)
    # 写入excel
    # 参数对应 行, 列, 值
    worksheet.write(0,0,label = '职位')
    worksheet.write(0,1,label = '地区')
    worksheet.write(0,2,label = '工资')
    worksheet.write(0,3,label = '公司')
 
    for i in range(len(position)):
        worksheet.write(i+1,0,position[i])
    # 把城市的信息保存在文件中，方便后面城市的统计
    with open("城市.txt",mode='w',encoding='utf-8') as f:
        for i in range(len(area)):
            worksheet.write(i+1,1,area[i])
            f.write(area[i])
    for i in range(len(salary)):
        worksheet.write(i+1,2,salary[i])
    for i in range(len(company)):
        worksheet.write(i+1,3,company[i])   
        
    # 保存
    workbook.save('C://Users//admin_peng//Desktop//职位信息爬虫.xls')
    dic = {'position':position,'area':area,'salary':salary,'company':company}
    return dic
def benDiBao():
    # s.proxies = {"https": "47.100.104.247:8080", "http": "36.248.10.47:8080", }
    # 获得主界面
    url = 'http://m.bendibao.com/city.php'
    page = requests.get(url=url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    page.encoding = 'gbk2312'
    soup = BeautifulSoup(page.text,'lxml')

    # 获得所有城市的超链接
    all_city_href = soup.find_all('div',attrs={'class':'col-xs-4 col-sm-3 col-md-2 col-lg-1'})
    city_name = []  # 存放城市名字
    city_href = []  # 存放城市的链接
    href_search = [] # 存放城市搜索栏的链接
    for city in all_city_href[250:]:
        city_name.append(city.get_text())
        city_href.append(city.a.get('href'))
#     city_name = set(city_name)
#     city_href = set(city_href)
#     city_name = list(city_name)
#     city_href = list(city_href)
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('本地宝首页')
    worksheet.write(0,0,label = '城市名字')
    worksheet.write(0,1,label = '城市本地宝的地址')
    worksheet.write(0,2,label = '搜索栏链接')
    for i in range(len(city_name)):
        worksheet.write(i+1,0,label=city_name[i])
        worksheet.write(i+1,1,label=city_href[i])
# 获得城市的搜索栏的链接
#     worksheet = workbook.add_sheet('搜索栏链接')

    print('失效的城市链接')
    a_search_href = ''
    for i in range(len(city_href)):
        try:
            page_son = requests.get(url=city_href[i],headers={'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'},verify=False)
            page_son.encoding = 'gbk2312'
            soup_son = BeautifulSoup(page_son.text, "html.parser")
            soup_son = soup_son.select(".search")
            if len(soup_son)!=0:
                a_search_href = soup_son[0].get('href')
                worksheet.write(i+1,2,label = a_search_href)  # 将搜索栏链接加入到表格中
                href_search.append(a_search_href)
            else :
                worksheet.write(i+1,2,label = '')  # 将搜索栏链接加入到表格中
                href_search.append('无')
                    
        except:
             worksheet.write(i+1,2,label = '')
             href_search.append('无')
            
#     通过拼接的方式来搜索相关资料
    information = '人才落户及补贴政策'
    worksheet.write(0,3,label = '政策1')
    worksheet.write(0,4,label = '政策2')
    for i in range(len(href_search)):
        try:
            if href_search[i]!='无':
                query_url = href_search[i].split('?')[0]+'?q='+information+'&click=1&'+href_search[i].split('?')[1]+'&nsid='
                page_search_result = requests.get(url=query_url,headers={'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'},verify=False)                
                soup_search_result = BeautifulSoup(page_search_result.text, "html.parser")
                worksheet.write(i+1,3,label = soup_search_result.select('.c-title')[0].a.get('href'))
                worksheet.write(i+1,4,label = soup_search_result.select('.c-title')[1].a.get('href'))
            else:
                worksheet.write(i+1,3,label = '')
                worksheet.write(i+1,4,label = '')
        except:
            worksheet.write(i+1,3,label = '')
            worksheet.write(i+1,4,label = '')
    workbook.save('C://Users//admin_peng//Desktop//城市本地宝相关信息.xls')   
    
    
def showJobInformation(job_name):

    # 处理薪资信息
    dic1 = getJop(job_name)
    salary = dic1['salary']
    dic_salary = deal_salary(salary)
    year_salary = dic_salary['year_salary'] # 年薪
    min_salary = min(year_salary)
    max_salary = max(year_salary)
    print(max_salary)
    print(min_salary)
    salary_each = (max_salary-min_salary)/5
    labels = []
    sizes = []
    size = 0
    for i in range(5):
        labels.append(""+(str(int(min_salary+i*salary_each)))+"~"+str(int(min_salary+(i+1)*salary_each)))
        for j in year_salary:
            if j>=int(min_salary+i*salary_each) and j<int(min_salary+(i+1)*salary_each):
                size += 1
        sizes.append(size/len(year_salary)*100)
    plot.title(job_name+'薪资分布')
    plot.pie(sizes,labels=labels)
    plot.show()

    # 处理地区信息
    area = dic1['area']
    areas = ''
    for i in area:
        areas += i
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式（空格等）
    areas = re.sub(pattern, '', areas)     # 将符合模式的字符去除
    # 文本分词
    seg_list_exact = jieba.cut(areas, cut_all=False, HMM=True)    # 精确模式分词+HMM
    word_counts = collections.Counter(seg_list_exact)       # 对分词做词频统计
    word_counts_top = word_counts.most_common(8)    # 获取前number个最高频的词
    print(word_counts_top)

    
def deal_salary(salary):
    n = 0 
    year_salary = []
    try:
        for s in salary:
            # 格式为面议
            if s=='面议':
                # year_salary.append(0)
                n += 1
            # 格式为10-12k'
            elif s.split('k')[1]=='' and s.split('-')[0].isdigit():
                min = int(s.split('-')[0])
                max = int(s.split('-')[1].split('k')[0])
                year_salary.append((min+max)*6)
            # 格式为40k
            elif s.split('k')[1]=='' and s.split('-')[0].isdigit()==False:
                min = int(s.split('k')[0])
                year_salary.append(min*12)
            # 40-70k·16薪
            elif s.split('-')[0].isdigit():
                min = int(s.split('-')[0])
                max = int(s.split('-')[1].split('k')[0])
                n = int(s.split('·')[1].split('薪')[0])
                year_salary.append((min+max)*n/2)
            # 30k·15薪
            else:
                min = int(s.split('k')[0])
                n = int(s.split('·')[1].split('薪')[0])
                year_salary.append(min*n)
    except:
        print("异常数据"+s)
    dic = {'year_salary':year_salary,'mianyi':n}
    return dic



if __name__ == "__main__":
    showJobInformation('算法')
    # benDiBao()
