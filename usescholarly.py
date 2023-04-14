from scholarly import scholarly
import pandas as pd
from fuzzywuzzy import fuzz

# 搜索所有摘要/标题/关键词中包括unlearn 的论文
search_query = scholarly.search_pubs('unlearn')

df = pd.read_csv('conferences.csv')



# 若会议名称在select_conf中，则将论文标题、会议名称和年份存入result
# result = []
with open('result.csv', 'w') as f:
    for pub in search_query:
        print(pub['bib']['title'])
        print(pub['bib']['venue'])
        max = 0
        for test in df['full_name'].values:
            ratio = fuzz.partial_ratio(pub['bib']['venue'], test)
            if ratio > max:
                max = ratio
            if ratio > 80:
                current = [pub['bib']['title'],
                           pub['bib']['venue'], pub['bib']['pub_year']]
                # result.append(current)
                f.write(current[0] + ',' + current[1] + ',' + str(current[2]) + '\n')
                # save
                break
        print(max)
        print('-----------------')
