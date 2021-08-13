import pandas as pd

sig_info = pd.read_csv('../Data_Crawel/SIG_Info/sig_repositories_maintainers_data.csv')
sig_name = sig_info['sig_name']
sig_repositories = sig_info['sig_repositories']
sig_maintainers = sig_info['sig_maintainers']
count = 0
json_sig, json_repositorie, json_user = [], [], []
for sig_name_ in sig_name:
    for sig_repositories_ in eval(sig_repositories[count]):
        # for user_name in eval(sig_maintainers[count]):
        json_sig.append(sig_name_)
        json_repositorie.append(sig_repositories_)
        # json_user.append(user_name)
    count += 1
sig_info_json = pd.DataFrame({
    'sig_name': json_sig,
    'sig_repositories': json_repositorie,
    # 'sig_maintainers': json_user
})
sig_info_json.to_csv('sig_info_json.csv', index=None)
