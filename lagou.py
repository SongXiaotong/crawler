import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import csv
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
from selenium import webdriver
import time

rb = open_workbook('lagou2.xls')
wb = copy(rb)



# 筛选过it分类后的内容
url='https://www.lagou.com/'
r=urllib.request.Request(url)
r.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')#模仿浏览器爬取，添加包头信息
html=urllib.request.urlopen(r).read()
# 获取数据页面中所有ul格式数据，在对内部的信息进行处理
cate_result = BeautifulSoup(html,"html.parser",from_encoding="utf-8")

cate1 = cate_result.findAll(name="div", attrs={"class":"menu_sub dn"})
sheet_num = 0;
# 类别
for jj in range(4):
    cate = cate1[jj]
    sheet = wb.get_sheet(jj)
    wb.save('lagou2.xls')
    curr = 0
    if jj < 3:  
        if jj != 0:
            cate = cate1[jj+2]
        if jj == 0:
            curr = 29742
        elif jj == 1:
            curr =3450
        else:
            curr = 1800
    else:
        cate = cate1[len(cate1)-1]
        sheet = wb.add_sheet('游戏')
        curr = 0
    catename = cate.find('span').get_text()
    print('正在爬取分类为'+catename+'的子类别')
    cate2 = cate.findAll('a')
    if jj < 3:
        if int(len(cate2)) < 22:
            num = int(len(cate2))
        else:
            num = 22
    else:
        num = int(len(cate2))
    
    for i in range(num):
        # 职位
        cate = ''
        if jj < 3:
            cate_ = cate2[len(cate2)-22+i]
        else:
            cate_ = cate2[i]
        link = cate_['href']
        category = cate_.get_text()
        print('====正在前往子分类为'+category+'的网址')
        try:
            r=urllib.request.Request(link)
            r.add_header('User-Agent','Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11')#模仿浏览器爬取，添加包头信息
            html=urllib.request.urlopen(r).read()
            page_result = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
            pages = page_result.findAll(name="a", attrs={"class":"page_no"})
            page = int(pages[len(pages)-2].get_text())
            #=========================================
            # page = 1
            #=========================================
            for i in range(page):
                print("========正在爬取第"+str(i+1)+"页的数据" + str(page))
                url = link+str(i+1)+'/?filterOption='+str(i+1)
                try:
                    r=urllib.request.Request(link)
                    r.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16')#模仿浏览器爬取，添加包头信息
                    html=urllib.request.urlopen(r).read()
                    result = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
                    lists = result.findAll(name="li", attrs={"class":"con_list_item default_list"})
                    num = 1
                    for list_ in lists:
                        job_name = list_['data-positionname']
                        # print(job_name)
                        job_comp = list_['data-company']
                        # print(job_comp)
                        job_sala = list_['data-salary']
                        # print(job_sala)
                        com_intr = list_.find(name="div", attrs={"class":"industry"}).get_text()
                        # print(com_intr)
                        job_regi = list_.find(name="span", attrs={"class":"add"}).get_text()
                        # print(job_regi)
                        job_expe = list_.find(name="div", attrs={"class":"p_bot"}).find(name="div", attrs={"class":"li_b_l"}).get_text()
                        # print(job_expe)
                        job_cates = list_.find(name="div", attrs={"class":"list_item_bot"}).find(name="div", attrs={"class":"li_b_l"}).findAll('span')
                        job_cate = ' '
                        for job_c in job_cates:
                            job_cate = job_cate + job_c.get_text() + ' '
                        # print(job_cate)
                        job_welf = list_.find(name="div", attrs={"class":"li_b_r"}).get_text()
                        # print(job_welf)
                        detail_link = list_.find(name="a", attrs={"class":"position_link"})['href']
                        job_deta = ''
                        # try:
                        #     r2=urllib.request.Request(detail_link)
                        #     time.sleep(2)
                        #     r2.add_header('User-Agent','Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11')#模仿浏览器爬取，添加包头信息
                        #     html2=urllib.request.urlopen(r2, timeout=5).read()
                        #     result2 = BeautifulSoup(html2,"html.parser")
                        #     print(result2)
                        #     job_deta = result2.find(name="dd", attrs={"class":"job_bt"}).find(name="div", attrs={"class":"job-detail"}).get_text()
                        #     # job_details = job_detail.findAll('p').get_text()
                        #     # for det in job_detail:
                        #     #     job_deta = job_deta + det.get_text()
                        # except ConnectionError:
                        #     print("============连接失败")
                        # except AttributeError:
                        #     print("！！！！！！！此页格式不符")
                        # except urllib.request.URLError:  
                        #     print("!!!")


                        # print(job_deta)
                        sheet.write(curr+1, 0, job_name)
                        sheet.write(curr+1, 1, job_comp)
                        sheet.write(curr+1, 2, job_sala)
                        sheet.write(curr+1, 3, job_regi)
                        sheet.write(curr+1, 4, job_expe)
                        sheet.write(curr+1, 5, job_cate)
                        sheet.write(curr+1, 6, job_welf)
                        # sheet.write(curr+1, 7, str(job_deta).strip())
                        sheet.write(curr+1, 7, com_intr)
                        curr = curr + 1
                        wb.save('lagou2.xls')
                        print("============第"+str(num)+'条记录成功')
                        num = num + 1
                except ConnectionError:
                    print("========获取第"+str(i+1)+"页[failed]")
                except Exception as e:
                    print("出现异常-->"+str(e))
                else:
                    print("========获取第"+str(i+1)+"页[success]")
        except Exception as e:
            print("出现异常-->"+str(e))