import pandas as pd

df = pd.read_json('res.txt', lines=True, encoding='utf-8')
df.to_csv('output.csv', sep=';', header=True, index=False, encoding='utf-8')
print(len(df), len(df.drop_duplicates(subset='url', keep='last')))
df.drop_duplicates(subset='url', keep='first').to_excel('output.xlsx')