import pandas as pd

data = pd.read_csv('Raw_data/Src-Openeuler-所有社区的信息.csv')
a = data.sort_values(by="watchers_count", axis=0, ascending=False)
print(a)
a.to_csv('Src-Openeuler-所有社区的信息.csv', index=None)
