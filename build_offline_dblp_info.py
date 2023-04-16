import pandas as pd
import requests
from scholarly import scholarly

def raw_dblp_info():
    result = []
    # 限制搜索范围
    search_url = f"https://dblp.org/search/publ/api?q=unlearn&h=1000&format=json"
    # 发送HTTP请求获取搜索结果
    response = requests.get(search_url)
    # 解析JSON格式的搜索结果
    result_json = response.json()
    for publ in result_json['result']['hits']['hit']:
        # 获取论文信息
        title = publ['info']['title']
        title = title.replace('.', '')
        key_parts = publ['info']['key'].split('/')
        conf_abbr = key_parts[0]
        subconf_abbr = key_parts[1]
        result.append([title, publ['info']['year'], conf_abbr, subconf_abbr])
    return result


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

def raw_dblp_from_google_scholar():
    search_query = scholarly.search_pubs('unlearn')
    result = []
    # open raw_result_dblp.csv with add mode
    with open('raw_result_dblp.csv', 'a') as f:
        for pub in search_query:
            year = pub['bib']['pub_year']
            title = pub['bib']['title']
            venue = pub['bib']['venue']
            print(title, year, venue)
            dblp_info = get_conference_info(title, year)
            if dblp_info is None:
                continue
            key_parts = dblp_info['info']['key'].split('/')
            conf_abbr = key_parts[0]
            subconf_abbr = key_parts[1]
            result.append([title, dblp_info['info']['year'], subconf_abbr])
            # csv add
            f.write(f"{title},{year},{conf_abbr},{subconf_abbr}\n")
            f.flush()
            print(f"{title},{year},{conf_abbr},{subconf_abbr}")
        

if __name__ == '__main__':
    raw_dblp_info()
    # raw_dblp_from_google_scholar()
