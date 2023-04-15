import csv
from crossref.restful import Works

# 读取会议列表
conferences = []
with open('conferences.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        conferences.append(row[0])

# 初始化Crossref API
works = Works()

# 搜索包含“unlearn”主题的论文（标题、摘要和关键词）
results = works.query(title='unlearn', abstract='unlearn', query='unlearn')

# 在结果中查找指定的会议
filtered_results = []
for result in results:
    if result['container-title'][0] in conferences:
        filtered_results.append(result)

# 将结果写入CSV文件
with open('results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Authors', 'Publication Date', 'Conference'])
    for result in filtered_results:
        title = result['title'][0]
        authors = ', '.join(author['given'] + ' ' + author['family']
                            for author in result['author'])
        date = result['created']['date-parts'][0]
        conference = result['container-title'][0]
        writer.writerow([title, authors, date, conference])
