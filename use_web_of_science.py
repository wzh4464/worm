import requests
import pandas as pd

# 从DBLP中获取会议的完整名称
def get_conference_info(name, year):
    name = name.replace(' ', '+')
    url = f"https://dblp.org/search/publ/api?q={name}+{year}&format=json"
    response = requests.get(url)
    if response is not None:
        result_json = response.json()
        if '0' is not result_json['result']['hits']['@total']:
            publ = result_json['result']['hits']['hit'][0]
            return publ
    return None


df = pd.read_csv('conferences.csv')
urls = df['url'].values

search_query = pd.read_csv('output.csv')

select_conf = []

# 解析URL中的会议和子会议缩写
for url in urls:
    url_parts = url.split('/')
    for part in url_parts:
        if part == 'db':
            conf_abbr = url_parts[url_parts.index(part) + 1]
            subconf_abbr = url_parts[url_parts.index(part) + 2]
            select_conf.append([conf_abbr, subconf_abbr])
            break

result = []

with open('result_web_of_science.csv', 'w') as f:
    for pub in search_query.itertuples():
        year = pub.year
        title = pub.title
        venue = pub.journal
        choose = False
        print(title, year, venue)
        dblp_info = get_conference_info(title, year)
        if dblp_info is None:
            continue
        key_parts = dblp_info['info']['key'].split('/')
        conf_abbr = key_parts[0]
        subconf_abbr = key_parts[1]
        print(conf_abbr, subconf_abbr)
        print('-' * 20)
        # if match select conf
        if [conf_abbr, subconf_abbr] in select_conf:
            result.append([title, dblp_info['info']['year'], subconf_abbr])
            choose = True
            venue = dblp_info['info']['venue']
        if choose:
            f.write(f"{year},{venue},{title}\n")
            # flush
            f.flush()