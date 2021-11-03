# Merges updated translated dataset (after review) with original dataset of notable schools
import pandas as pd
import pickle
import re
import ast

# Loads the dataset corresponding to notable schools
def load_notable_schools_df():
    a = pd.DataFrame()
    with open(f'./scrape_new_data/notable_schools_org_data.pkl', 'rb') as f:
        a = pickle.load(f)
    return a

# Updates the nearby schools attribute including necessary translation
def update_nearby_schools(previous_data, new_data):
    final_data = []
    for i in range(len(previous_data)):
        prev_list, trans_list, curr_list = ast.literal_eval(previous_data[i]), ast.literal_eval(new_data[i]), []
        for j in range(len(prev_list)):
            url = re.split('\s*\#\$\#\s*', prev_list[j])[1]
            school_name = trans_list[j]
            curr_list.append(school_name + ' #$# ' + url)
        final_data.append(curr_list)
    return final_data

b = load_notable_schools_df()
with open(f'./scrape_new_data/translated_dataset_notable_schools.pkl', 'rb') as f:
    a = pickle.load(f)

all_cols = b.columns.tolist()
translated_cols = a.columns.tolist()
to_drop = [col for col in all_cols if col in translated_cols and col != 'School Code']
print(len(to_drop))
print(to_drop)
b.drop(columns=to_drop, inplace=True)
a['School Code'] = a['School Code'].astype(int)
b['School Code'] = b['School Code'].astype(int)
a['nearby_schools_Telugu'] = update_nearby_schools(b['Nearby Schools'].tolist(), a['nearby_schools_Telugu'].tolist())
a.drop(columns=['nearby_schools'], inplace=True)
print(b.shape)
print(a.shape)
b = pd.merge(b, a, on='School Code')
a = b
print(a.shape)
a.to_excel('./scrape_new_data/notable_schools_org_data.xlsx', index=False)
with open('./scrape_new_data/notable_schools_org_data.pkl', 'wb') as f:
    pickle.dump(a, f)
    