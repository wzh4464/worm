import pandas as pd

# merge two csv
df1 = pd.read_csv('title_result.csv')
df2 = pd.read_csv('result_web_of_science.csv')

# df1 and df2 have the same column name, but different order
merged_df = pd.concat([df1, df2], axis=0)

# remove all commas in the title column
merged_df['title'] = merged_df['title'].str.replace('.', '')

# extract and print duplicates
duplicates = merged_df[merged_df.duplicated(subset=['title'], keep=False)]
print('Duplicate rows:')
print(duplicates)

# drop duplicate rows
merged_df.drop_duplicates(subset=['title'], inplace=True)

# set the first row as header row and skip sorting
merged_df.to_csv('merged.csv', index=False, header=True, mode='w')
