import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import csv
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

#初始化并创建一个工作簿
rb = open_workbook('job.xls')
wb = copy(rb)
sheet = wb.get_sheet(0)


# 筛选过it分类后的内容
url='http://s.cjol.com/?SearchType=4&Industry=7008-7175-7180'

#获取页面数，然后处理

print('start!')

curr = 5520

for page in range(9):
    id = 139 + page
    print('开始抓取第' + str(id) + '页的数据')
    postdata=urllib.parse.urlencode({'page':page+1}).encode('utf-8')#用字典保存索要注册的信息并用urlencode编码，使用encode（）设置utf-8编码格式
    r=urllib.request.Request(url,postdata)
    r.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')#模仿浏览器爬取，添加包头信息
    data=urllib.request.urlopen(r).read()
    # 获取数据页面中所有ul格式数据，在对内部的信息进行处理
    soup = BeautifulSoup(data,"html.parser",from_encoding="utf-8")
    searchlist = soup.findAll(name="ul", attrs={"class":"results_list_box"})
    # 得到一页中所有的记录的个数
    num_in_page = len(searchlist)
    # print(num_in_page)

    # num_in_page = 3

    for i in range(num_in_page):
        try:
            print()
            job_name = searchlist[i].find(name="li", attrs={"class":"list_type_first"}).find("h3").get_text()
            # print(job_name)
            job_comp = searchlist[i].find(name="li", attrs={"class":"list_type_second"}).get_text()
            job_regi = searchlist[i].find(name="li", attrs={"class":"list_type_third"}).get_text()
            job_grad = searchlist[i].find(name="li", attrs={"class":"list_type_fifth"}).get_text()
            job_expe = searchlist[i].find(name="li", attrs={"class":"list_type_sixth"}).get_text()
            job_sala = searchlist[i].find(name="li", attrs={"class":"list_type_seventh"}).get_text()
            # print(job_name + ' ' + job_comp + ' ' + job_regi + ' ' + job_grad + ' ' + job_expe + ' ' + job_sala)
               
            detailurl = searchlist[i].find(name="li", attrs={"class":"list_type_first"}).find('a')['href']
                
                
            r2=urllib.request.Request(detailurl,postdata)
            r2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')#模仿浏览器爬取，添加包头信息
            detail=urllib.request.urlopen(r2).read()
            de_result = BeautifulSoup(detail,"html.parser",from_encoding="utf-8")

            job_detail = de_result.find(name="div", attrs={"class":"coninfo-jobdesc"}).findAll('p')
            job_deta = ' '
            for detail_ in job_detail:
                job_deta =  job_deta + ' ' + detail_.get_text()

            sheet.write(curr+1, 0, job_name)
            sheet.write(curr+1, 1, job_comp)
            sheet.write(curr+1, 2, job_regi)
            sheet.write(curr+1, 3, job_grad)
            sheet.write(curr+1, 4, job_expe)
            sheet.write(curr+1, 5, job_sala)
            sheet.write(curr+1, 6, job_deta)
            curr = curr + 1
            wb.save('job.xls')
        except IOError:
            print('    第' + str(i) + '条记录 ' + 'something error! ')
        else:
            print('    第' + str(i) + '条记录 ' + 'success! ')



# f=open('E:/1.html','wb')
# f.write(data)
# f.close()s