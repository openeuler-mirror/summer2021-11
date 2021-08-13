import pandas as pd

comment_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv')
#commenter,creator,issue_id,body,label,comment_time
comments_username = comment_data['commenter']
creator = comment_data['creator']