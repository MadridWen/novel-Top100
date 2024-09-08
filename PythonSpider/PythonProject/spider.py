# -*- coding:utf-8 -*-
import sqlite3
import urllib.request
import urllib.error
from http.client import HTTPResponse
from bs4 import BeautifulSoup
import re
import xlwt

# 全局变量--start
baseurl = 'https://www.qidian.com/rank/hotsales/'

# 检索小说信息的正则表达式
# 书名
findTitle = re.compile(r'data-eid="qd_C40".*>(.*?)</a></h2>', re.S)
# 书作者
findWri = re.compile(r'<p class="author">(.*?)</p>', re.S)
# 书详情链接
findlink = re.compile(r'<h2><(.*?)></h2>')
# 书简介
findInq = re.compile(r'<p class="intro">(.*?)</p>')
# 书封面图片
findPic = re.compile(r'<img.*src="(.*?)"', re.S)


# 全局变量--end

# 主函数--start
def main():
    # 1.获取网页数据
    htmllist = getData(baseurl, 10, 10)
    # print(htmllist)

    # 2.解析内容
    datalist = getText(htmllist)  # 除图片外列表
    # piclist = getPicture(htmllist)  # 图片列表
    finaldata = datalist  # + piclist  # 拼接
    # print(type(finaldata))
    # for item in datalist:
    #     print(item)
    # print(finaldata)

    # 3.保存数据
    savepath = '起点中文网畅销榜Top100.xls'
    # 保存到Excel表格
    saveDataExcel(finaldata, savepath)
    # 保存到SQLite数据库
    # 指定数据库文件的路径
    dbpath = '../novel.db'
    saveDataSQlite(finaldata, dbpath)
    create_team_table(dbpath)



# 主函数--end

# 功能函数--start


# 1.获取数据
# baseurl 网页网址
# page   一共多少页
# strip  每页多少条
def getData(baseurl, page, strip):
    # 创建一个列表来存网页源码信息，1页，存一个元素
    datalist = []
    # 调用获取网页信息的函数askURL()10次，然后统统存到datalist里面
    for i in range(0, page):
        # 每次获取10条，一共100条数据
        # 对网页网址url进行拼接，
        url = baseurl + str(i * strip)
        # 调用askURL()函数，获取网页源码
        html = askURL(url)
        datalist.append(html)
    return datalist


# 2.解析网页内容
def getText(htmllist):
    # 创建一个列表，datalist，存所有的小说信息
    datalist = []
    for html in htmllist:
        # 一条一条的解析，一个网页一个网页的解析
        soup = BeautifulSoup(html, 'html.parser')
        # 对每一页网页，里面所有需要的小说信息进行循环。
        for item in soup.find_all('div', class_='book-mid-info'):
            # 创建一个列表，data用来保存每一个小说中，每一条信息
            data = []
            # 把item转换成字符串类型，然后使用正则表达式，筛选需要的数据
            item = str(item)

            # 获取书名
            title = re.findall(findTitle, item)[0]
            # 强制类型转换成字符串
            # finaltitle = str(title)
            # 防止单个索引值超出上限报错
            # var = len(title) != 0
            # finaltitle = title[0]
            # 把书详情追加到data列表中
            # data.append(finaltitle)
            data.append(title)
            # print(title)

            '''
            writer = re.findall(findWri, item)[0]
            # var = len(writer) != 0
            # finalwriter = writer[0]
            # data.append(finalwriter)
            fwriter = re.findall(r'<a class="name" href="" target="_blank" data-eid="qd_C41">(.*?)</a>',writer)
            data.append(fwriter)
            print(fwriter)

            link = re.findall(findlink, item)[0]
            # var = len(link) != 0
            # finallink = link[0]
            # data.append(finallink)
            flink = re.findall(r'<a href="(.*?)" target="_blank" data-eid="qd_C40" data-bid="" title="">*</a>',link)
            data.append(flink)
            print(flink)
            #print(type(link))
            '''

            # 书图片
            # pic = re.findall(findPic, item)[0]
            # data.append(pic)

            inq = re.findall(findInq, item)[0]
            data.append(inq)
            # print(inq)

            datalist.append(data)
    return datalist


def getPicture(htmllist):
    piclist = []
    for html in htmllist:
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='book-mid-info'):
            data = []
            # 书图片
            pic = re.findall(findPic, item)[0]
            data.append(pic)
            piclist.append(data)
        return piclist


# 3.保存数据
# 3.1保存数据到Excel表格，我们需要引入xlwt模块
def saveDataExcel(finaldata, savepath):
    print('保存数据到excel表格.......')
    # 表示单元格是否压缩，是否允许改变excl表格的样式
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # cell_overwrite_ok=True 允许多次写入，如果是False，多次写入会发生异常
    worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    # 创建一个元组，用来指定表格数据的标题
    col = ('小说书名', '小说简介')
    # 把标题循环添加到excel表格
    for i in range(0, len(col)):
        worksheet.write(0, i, col[i])  # 列名
    # 把爬取到的小说信息添加到Excel表格
    # 循环添加，长度为100，finaldata的长度
    for i in range(0, len(finaldata)):
        print('第%d条' % (i + 1))
        # 为每一部小说的信息分别添加到每一行的每一个单元格当中
        data = finaldata[i]
        for j in range(len(data)):
            worksheet.write(i + 1, j, data[j])  # 数据
    workbook.save(savepath)

# 3.2保存数据到SQLite数据库，我们需要引入sqlite3模块
def saveDataSQlite(finaldata, dbpath):
    #sql_createTable
    creatQeSql = "create table noveltop100 (id integer primary key autoincrement,title text,writer text)"
    #sql_inte_sqllite
    init_db(dbpath, creatQeSql)
    sql_lite = sqlite3.connect(dbpath)
    cur = sql_lite.cursor()
    for data in finaldata:
        insert_sql = f'insert into noveltop100(title,writer) values("{data[0]}","{data[1]}")'
        cur.execute(insert_sql)
    sql_lite.commit()
    cur.close()
    sql_lite.close()

def create_team_table(c_path):
    creatQeSql = "create table team (id integer primary key,name text,gender text,age text,class text,identity text,imgurl text)"
    sql_lite = sqlite3.connect(c_path)
    sql_lite.execute('drop table if exists team')
    sql_cur = sql_lite.cursor()
    sql_cur.execute(creatQeSql)
    sql_lite.commit()
    menber_list = [
        ['"21042222"','"王天一"','"男"','"18"','"计算机科学与技术2班"','"组长"','"/static/picture/img_hend_1.jpg"'],
        ['"21042221"','"王广辰"','"男"','"18"','"计算机科学与技术2班"','"组员"','"/static/picture/img_hend_2.jpg"'],
        ['"21042224"','"王雨璐"','"女"','"18"','"计算机科学与技术2班"','"组员"','"/static/picture/img_hend_3.jpg"'],
        ]
    for menber_item in menber_list:
        insert_sql = f'insert into team(id,name,gender,age,class,identity,imgurl) values({",".join(menber_item)})'
        sql_cur.execute(insert_sql)
    sql_lite.commit()
    sql_cur.close()
    sql_lite.close()

# 初始化数据库--根据给定的sql语句，和数据库地址创建数据库表
def init_db(dbpath, sql):
    # 创建数据库
    sql_lite = sqlite3.connect(dbpath)
    sql_lite.execute('drop table if exists noveltop100')
    cur = sql_lite.cursor()
    cur.execute(sql)
    sql_lite.commit()
    cur.close()
    sql_lite.close()


# 得到指定的网页内容
# url    网页网址
def askURL(url):  # 打开网页，向网页服务器发送请求，获取网页所有源码信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'
    }
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 创建一个字符串变量存html内容
    html = ''
    try:
        response = urllib.request.urlopen(req)
        assert isinstance(response, HTTPResponse)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html


# 功能函数--end

if __name__ == '__main__':
    main()
