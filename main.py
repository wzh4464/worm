import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_sub_conference_urls(conference_url):
    response = requests.get(conference_url)
    soup = BeautifulSoup(response.content, "html.parser")
    urls = [a["href"]
            for a in soup.find_all("a", href=True) if "conf" in a["href"]]
    return urls


# 读取csv文件并存储为pandas dataframe
df = pd.read_csv('conferences.csv')

# 遍历每一行，爬取对应网址的页面，并获取包含关键词的论文标题
for index, row in df.iterrows():
    # 获取会议简称和网址
    conf_abbr = row['abbreviation']
    conf_url = row['url']

    # 获取主会议页面上所有子会议页面的链接
    sub_urls = get_sub_conference_urls(conf_url)

    # 遍历每个子会议页面
    for sub_url in sub_urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(sub_url)
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 在XML文档中查找所有包含关键词的标题，并保存到列表中
        titles = []
        for hit in soup.find_all('hit'):
            title = hit.find('title')
            if title and 'unlearn' in title.text.lower():
                titles.append(title.text.strip())

        # 如果找到了包含关键词的标题，打印出来
        if len(titles) > 0:
            print(f"{conf_abbr}: {sub_url}: {', '.join(titles)}")
