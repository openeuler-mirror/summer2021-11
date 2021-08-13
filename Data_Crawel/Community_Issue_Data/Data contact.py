import pandas as pd


def concat_Raw_data():
    data1 = pd.read_csv('Raw_data/Openeuler_issue_comment.csv')
    data2 = pd.read_csv('Raw_data/Src-Openeuler_issue_comment.csv')
    data3 = pd.concat([data1, data2], axis=0)
    data3.to_csv('Openeuler+Src_all_issue_comment.csv', index=False)


concat_Raw_data()
