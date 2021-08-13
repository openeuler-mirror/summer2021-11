import pandas as pd

community_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/Raw_data/Openeuler-所有社区的信息.csv')
forks_count = community_data['forks_count']
stargazers_count = community_data['stargazers_count']
watchers_count = community_data['watchers_count']
open_issues_count = community_data['open_issues_count']
community_name = community_data['name']
