import requests
import pandas as pd

df = pd.read_csv('conferences.csv')

# 搜索关键词
keywords = 'unlearn'

# 构建API请求URL
url = f'https://dblp.org/search/publ/api?q={keywords}&h=1000&format=json'

# 发送HTTP请求并获取搜索结果
response = requests.get(url)
data = response.json()

# with open('titles.txt', 'w') as f:
#     # 处理搜索结果，获取包含关键词的论文标题
#     for hit in data['result']['hits']['hit']:
#         title = hit['info']['title']
#         conf = hit['info']['venue']
#         if keywords in title.lower():
#             if conf in df['abbreviation'].values:
#                 # 将论文标题写入文件
#                 f.write(f"{title} ({conf})\n")
#             if conf in df['full_name'].values:
#                 # 将论文标题写入文件
#                 f.write(f"{title} ({conf})\n")

# save to a df, titles and confs
result = []

for hit in data['result']['hits']['hit']:
    title = hit['info']['title']
    conf = hit['info']['venue']
    if keywords in title.lower():
        result.append([title, conf])

# save df to a result.csv
df = pd.DataFrame(result, columns=['title', 'conf'])
df.to_csv('result.csv', index=False)