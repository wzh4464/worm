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
    nameplus = name.replace(' ', '+')
    url = f"https://dblp.org/search/publ/api?q={nameplus}+{year}&format=json"
    response = requests.get(url)
    if response is not None:
        result_json = response.json()
        if '1' is result_json['result']['hits']['@total']:
            publ = result_json['result']['hits']['hit'][0]
            return publ
        if '0' is not result_json['result']['hits']['@total']:
            with open('mult_.txt', 'a') as f:
                f.write(f"{name},{year}\n")
    return None

def raw_dblp_from_google_scholar():
    search_query = scholarly.search_pubs('unlearn')
    result = []
    now = 0
    for pub in search_query:
        now += 1
        year = pub['bib']['pub_year']
        title = pub['bib']['title']
        venue = pub['bib']['venue']
        # print(title, year, venue)
        # 显示进度
        print(f"now: {now}/", search_query.total_results)
        # if 省略号 in venue or title: pause and wait my order
        if '…' in title:
            with open('pause.txt', 'a') as f:
                f.write(f"{title},{year},{venue}")
        dblp_info = get_conference_info(title, year)
        if dblp_info is None:
            continue
        key_parts = dblp_info['info']['key'].split('/')
        conf_abbr = key_parts[0]
        subconf_abbr = key_parts[1]
        result.append([title, dblp_info['info']['year'], conf_abbr, subconf_abbr])
        print(f"{title},{year},{conf_abbr},{subconf_abbr}")
    # 保存结果
    df = pd.DataFrame(result, columns=['title', 'year', 'conf_abbr', 'subconf_abbr'])
    df.to_csv('raw_dblp_from_google_scholar.csv', index=False)
        
def raw_dblp_from_wos():
    df = pd.read_csv('web_of_science.csv')
    result = []
    now = 0
    for title, year in zip(df['title'], df['year']):
        now += 1
        dblp_info = get_conference_info(title, year)
        if dblp_info is None:
            continue
        key_parts = dblp_info['info']['key'].split('/')
        conf_abbr = key_parts[0]
        subconf_abbr = key_parts[1]
        result.append([title, dblp_info['info']['year'], conf_abbr, subconf_abbr])
        print(f"{title},{year},{conf_abbr},{subconf_abbr}")
        print(f"now: {now}/{len(df)}")
    # 保存结果
    df = pd.DataFrame(result, columns=['title', 'year', 'conf_abbr', 'subconf_abbr'])
    df.to_csv('raw_dblp_from_wos.csv', index=False)


# for url in urls:
#     url_parts = url.split('/')
#     for part in url_parts:
#         if part == 'db':
#             conf_abbr = url_parts[url_parts.index(part) + 1]
#             subconf_abbr = url_parts[url_parts.index(part) + 2]
#             select_conf.append([conf_abbr, subconf_abbr])
#             break

def get_select_conf():
    df = pd.read_csv('A_conference.csv')
    urls = df['url'].values
    select_conf = []
    for url in urls:
        url_parts = url.split('/')
        for part in url_parts:
            if part == 'db':
                conf_abbr = url_parts[url_parts.index(part) + 1]
                subconf_abbr = url_parts[url_parts.index(part) + 2]
                select_conf.append([conf_abbr, subconf_abbr])
                break
    return select_conf

def pick_csv_from_select(csv_file, select_conf):
    df_paper = pd.read_csv(csv_file)
    df_conf = pd.DataFrame(select_conf, columns=['conf_abbr', 'subconf_abbr'])
    # if items in df_paper coincide with items in df_conf, then keep it
    df_paper = df_paper[df_paper['conf_abbr'].isin(df_conf['conf_abbr'])]
    df_paper = df_paper[df_paper['subconf_abbr'].isin(df_conf['subconf_abbr'])]
    df_paper.to_csv('paper_from_now.csv', index=False)

if __name__ == '__main__':
    # raw_dblp_info()
    # raw_dblp_from_google_scholar()
    # raw_dblp_from_wos()
    select_conf = get_select_conf()
    pick_csv_from_select('now.csv', select_conf)
    # save 
    # df = pd.DataFrame(select_conf, columns=['conf_abbr', 'subconf_abbr'])
    # df.to_csv('select_conf.csv', index=False)
