import pandas as pd

# 读取文件并保存为DataFrame
with open('dataset.txt') as f:
    lines = f.readlines()

rows = []
for line in lines:
    if line.startswith('PT J') or line.startswith('PT C'):
        rows.append({})
    if line.startswith('TI'):
        rows[-1]['title'] = line[3:].strip()
    if line.startswith('SO'):
        rows[-1]['journal'] = line[3:].strip()
    if line.startswith('PY'):
        rows[-1]['year'] = line[3:].strip()
    if line.startswith('EA'):
        ea_value = line[3:].strip()
        if ea_value != '':
            rows[-1]['year'] = ea_value[-4:]

df = pd.DataFrame(rows)
# df = df.drop(columns=['date'])  # 去掉date列

# 保存为csv文件
df.to_csv('web_of_science.csv', index=False)
