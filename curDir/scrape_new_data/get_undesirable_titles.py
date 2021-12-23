import pandas as pd
import pickle

with open('./notable_schools_org_data.pkl', 'rb') as f:
    a = pickle.load(f)
req_cols = ['School Title', 'School Title_Telugu']
telugu_titles_list = a['School Title_Telugu'].tolist()
titles_list = a['School Title'].tolist()
codes = a['School Code'].tolist()
data = []
for i in range(len(telugu_titles_list)):
    if 'పాఠశాల' in telugu_titles_list[i] or 'భవన్' in telugu_titles_list[i] or 'విద్యాలయ' in telugu_titles_list[i]:
        continue
    data.append([titles_list[i], telugu_titles_list[i], codes[i]])
df = pd.DataFrame(data, columns=req_cols + ['School Code'])
print(df.shape)
df.to_excel('titles.xlsx')