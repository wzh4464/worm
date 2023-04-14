import pandas as pd
import requests
from bs4 import BeautifulSoup

# 读取csv文件并存储为pandas dataframe
df = pd.read_csv('conferences.csv')

# 提取df中url
urls = df['url'].values

# url 按 ‘/’ 分割，取 db 后的两个元素
# 例如：https://dblp.org/db/conf/icml/icml2020.html
# 则取 conf 和 icml

select_conf = []

for url in urls:
    url_parts = url.split('/')
    for part in url_parts:
        if part == 'db':
            conf_abbr = url_parts[url_parts.index(part) + 1]
            subconf_abbr = url_parts[url_parts.index(part) + 2]
            select_conf.append([conf_abbr, subconf_abbr])
            break



result = []

# for hit in data['result']['hits']['hit']:
#     title = hit['info']['title']
#     conf = hit['info']['venue']
#     if keywords in title.lower():
#         result.append([title, conf])

# save df to a result.csv
# df = pd.DataFrame(result, columns=['title', 'conf'])
# df.to_csv('result.csv', index=False)
# 遍历每一行，爬取对应网址的页面，并获取包含关键词的论文标题、摘要和关键词


# 限制搜索范围
search_url = f"https://dblp.org/search/publ/api?q=unlearn&h=1000&f=abstracts&f=title&f=keywords&format=json"

# 发送HTTP请求获取搜索结果
response = requests.get(search_url)
# 解析JSON格式的搜索结果
result_json = response.json()
# 遍历搜索结果中的每篇论文
for publ in result_json['result']['hits']['hit']:
    # 获取论文信息
    title = publ['info']['title']
    key_parts = publ['info']['key'].split('/')
    conf_abbr = key_parts[0]
    subconf_abbr = key_parts[1]
    # if match select conf
    if [conf_abbr, subconf_abbr] in select_conf:
        result.append([title, publ['info']['year'], subconf_abbr])

# save result to a result.csv
result_df = pd.DataFrame(result, columns=['title', 'conf_abbr', 'subconf_abbr'])
result_df.to_csv('result.csv', index=False)
        
