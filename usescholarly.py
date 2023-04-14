import requests
import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
import pandas as pd
from scholarly import scholarly

# 从DBLP中获取会议的完整名称和年份信息


def get_conference_info(name, year):
    url = f"https://dblp.org/search/publ/api?q={name} {year}&h=1000&format=xml"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    for hit in root.iter('hit'):
        info = hit.find('info')
        if info is not None:
            venue_elem = info.find('venue')
            year_elem = info.find('year')
            if venue_elem is not None and year_elem is not None and year_elem.text == year:
                return venue_elem.text, year
    return None, None


df = pd.read_csv('conferences.csv')
search_query = scholarly.search_pubs('unlearn')

with open('result.csv', 'w') as f:
    for pub in search_query:
        venue = pub['bib']['venue']
        year = pub['bib']['pub_year']
        full_name = ''
        # 首先尝试精确匹配
        if venue in df['full_name'].values:
            full_name = df.loc[df['full_name'] == venue, 'full_name'].iloc[0]
        else:
            # 如果无法精确匹配，则从DBLP中获取完整的会议名称和年份信息
            abbr = venue.split()[-1]
            dbpl_name, dbpl_year = get_conference_info(abbr, year)
            # 使用模糊匹配算法匹配完整的会议名称
            if dbpl_name is not None and dbpl_year is not None:
                max_similarity = 0
                for name in df['full_name'].values:
                    similarity = fuzz.token_set_ratio(dbpl_name, name)
                    if similarity > max_similarity:
                        max_similarity = similarity
                        full_name = name
        if full_name:
            f.write(f"{pub['bib']['title']},{full_name},{year}\n")
