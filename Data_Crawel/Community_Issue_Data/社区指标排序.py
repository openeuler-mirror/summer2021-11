import pandas as pd

community_data = pd.read_csv('Raw_data/Openeuler-所有社区的信息.csv')

watchers_count = community_data['watchers_count']
stargazers_count = community_data['stargazers_count']
forks_count = community_data['forks_count']
print(community_data.sort_values(by="watchers_count", ascending=False))
print(print(community_data.sort_values(by="watchers_count", ascending=False)['name']))