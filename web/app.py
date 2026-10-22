from flask import Flask, render_template  # 引入render_template模块
import sqlite3

app = Flask(__name__)


# http://127.0.0.1:5000/  浏览器会根据装饰器中的''参数进行匹配对应的视图函数
@app.route('/')  # 装饰器，根据它来找对应的视图函数
def index():  # 视图函数  主页
    # 返回一个render_template('index.html')函数
    return render_template('index.html')


# 小说列表页面
@app.route('/novel')
def novel():  # 读取数据库中的数据，把数据展示到网页中。

    # 创建一个列表novels，用来存小说信息
    novels = []
    # 指定要打开的数据库  创建数据库连接
    conn = sqlite3.connect('novel.db')
    # 创建游标
    cur = conn.cursor()
    # 编写sql语句
    sql = 'select title,writer from noveltop100;'
    # 执行sql语句，查询表中的数据记录
    datas = cur.execute(sql)
    # 循环，取出每一条记录的每一个数据
    for item in datas:
        novels.append(item)
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    conn.close()
    return render_template('novel.html', novels=novels)


# 词云页面
@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')


# 团队页面
@app.route('/team')
def team():
    myTeam = []
    conn = sqlite3.connect('novel.db')
    cur = conn.cursor()
    sql = 'select id,name,gender,age,class,identity,imgurl from team;'

    datas = cur.execute(sql)
    for item in datas:
        myTeam.append(item)
    cur.close()
    conn.close()
    return render_template('team.html', myTeam=myTeam)


if __name__ == '__main__':
    app.run()
