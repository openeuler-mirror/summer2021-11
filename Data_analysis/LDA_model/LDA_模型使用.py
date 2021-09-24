from .LDA2 import LDA2
import pandas as pd

oe_closed_data = pd.read_csv('../../Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv')
title = oe_closed_data['title']
issue_id = oe_closed_data['issue_id']
label = oe_closed_data['label']
issue_url = oe_closed_data['issue_url']

