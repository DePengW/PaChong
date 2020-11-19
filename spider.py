
#!/usr/bin/env python
# encoding: utf-8


from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3

def main():
    baseurl = "https://movie.douban.com/top250?start="

    # 1.爬取数据
    datalist = getData(baseurl)
    # savepath = "豆瓣电影Top250.xls"
    savepathdb = "movie.db"
    # 3.保存数据
    # saveData(datalist, savepath)
    saveDataDB(datalist, savepathdb)


findLink = re.compile(r'<a href="(.*?)">')      # 找链接的pattern
findImg = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')    # 评分指标
findJudge = re.compile(r'<span>(\d*)人评价</span>')     # 评价
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

# 根据url，获得指定信息
def getData(baseurl):
    datalist = []
    for i in range(0, 1):
        url = baseurl + str(i*25)
        html = askURL(url)          # 保存html源码

        # 2.解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            # print(item)

            data = []
            item = str(item)

            # 使用正则表达式解析数据
            link = re.findall(findLink, item)[0]
            data.append(link)

            imgSrc = re.findall(findImg, item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle, item)
            if(len(titles) == 2):
                ctitile = titles[0]
                otitile = titles[1]
                data.append(ctitile)
                data.append(otitile)
            else:
                ctitile = titles[0]
                otitile = ""
                data.append(ctitile)
                data.append(otitile)

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)[0]
            if len(inq) != 0:
                inq = inq.replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', "", bd)
            data.append(bd.strip())

            datalist.append(data)
    return datalist


# 得到一个url的指定内容
def askURL(url):

    # 用户代理，模拟浏览器头部信息，想豆瓣服务器发消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    # 发送url请求
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        # 接受响应
        response= urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html



def saveData(datalist, savepath):
    print("save...")
    # 创建一个xml对象
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 插入页签
    sheet = book.add_sheet("豆瓣top250")
    cols = ("电影详情链接", "图片链接", "影片中文名", "外国名", "评分", "评价数","概况","相关信息")
    # 写入内容
    for i in range(8):
        sheet.write(0, i, cols[i])

    for i in range(len(datalist)):
        print("第{0}条".format(i+1))
        for j in range(0, 8):
            sheet.write(i+1, j, datalist[i][j])

    book.save(savepath)



def saveDataDB(datalist, savepathdb):
    # 初始化数据库，创建表
    init_db(savepathdb)
    # 连接数据库
    conn = sqlite3.connect(savepathdb)
    # 创建游标
    c = conn.cursor()
    # 编写sql语句
    sql = ""
    for data in datalist:
        for idx in range(len(data)):
            if idx is 4 or idx is 5:
                continue
            data[idx] = '"' + data[idx] + '"'
        sql = '''
            insert into movie250 (info_link, pic_link, cname, ename, score, rated, instroduction, infor) 
            values(%s)'''%",".join(data)
        print(sql)
        # 执行sql语句
        c.execute(sql)
        # 提交数据库操作
        conn.commit()
    # 关闭数据库
    c.close()


def init_db(savepathdb):
    conn = sqlite3.connect(savepathdb)
    c = conn.cursor()
    sql = '''
         create table movie250
        (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric,
            rated numeric,
            instroduction text,
            infor text
        )
    '''

    c.execute(sql)

    conn.commit()

    conn.close()



if __name__ == "__main__":
    main()
    print("over")