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

    sub_url = get_sub_conference_urls(conf_url)

    for url in sub_url:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # 在HTML中查找所有标题，并保存包含关键词的标题
        titles = []
        for h in soup.find_all('h4'):
            # 白色输出，如果包含关键字，则使用红色输出
            if 'unlearn' in h.text.lower():
                print('\033[31m' + h.text + '\033[0m')
                titles.append(h.text)
            else:
                print(h.text)
