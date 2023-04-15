# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlwt
from time import sleep
from tqdm import tqdm

TotalNum = 0


class Article(object):
    title = ""
    article_link = ""
    authors = ""
    authors_link = ""
    abstract = ""

    def __init__(self):
        title = "New Paper"


def save_xls(sheet, paper):
    # 将数据按列存储入excel表格中
    global TotalNum
    sheet.write(TotalNum, 0, TotalNum)
    sheet.write(TotalNum, 1, paper.title)
    sheet.write(TotalNum, 2, paper.article_link)
    sheet.write(TotalNum, 3, paper.journal)
    sheet.write(TotalNum, 4, paper.authors_link)
    sheet.write(TotalNum, 5, paper.abstract)
    TotalNum += 1


def GetInfo(sheet, url):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }  # 20210607更新，防止HTTP403错误
    r = requests.get(url, headers=head)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    articles = soup.find_all(class_="gs_ri")
    for article in articles:
        paper = Article()
        try:
            title = article.find('h3')
            paper.title = title.text
            # print(paper.title)
            paper.article_link = title.a.get('href')
            # print(paper.article_link)

            journal = article.find('div', {'class': 'gs_a'}).text.strip()
            journal = journal.split('-')[1].strip()
            journal = journal.split(',')[0].strip()
            journal = ' '
            
            if ''


            paper.journal = journal.text
            # print(paper.authors)
            authors_addrs = journal.find_all('a')
            for authors_addr in authors_addrs:
                # print(authors_addr.get('href'))
                paper.authors_link = paper.authors_link + \
                    (authors_addr.get('href'))+"\n"

            abstract = article.find(class_="gs_rs")
            paper.abstract = abstract.text
            # print(paper.abstract)
        except:
            continue
        save_xls(sheet, paper)
    return


if __name__ == '__main__':
    myxls = xlwt.Workbook()
    sheet1 = myxls.add_sheet(u'PaperInfo', True)
    column = ['序号', '文章题目', '文章链接', '期刊', '作者链接', '摘要']
    for i in range(0, len(column)):
        sheet1.write(TotalNum, i, column[i])
    TotalNum += 1

    keyword = input("keywords is?\n")
    # keyword = diabetes and conjunctiva and (microcirculation or microvasculature)
    print(keyword)
    key = keyword.replace(" ", "+")
    start = 0
    for i in tqdm(range(10)):
        url = 'https://xs.dailyheadlines.cc/scholar?start=' + \
            str(start) + '&q=' + key + '&hl=zh-CN&as_sdt=0,5'
        start = start + 10
        GetInfo(sheet1, url)
        myxls.save(keyword+'_PaperInfo.xls')
        sleep(0.5)
    print("检索完成")
