# Generates translated dataset (for review) for notable schools
import pandas as pd
import pickle
import sys
import time
from write import get_translated_data

def main():
    CHUNK_SIZE = 2500
    a = pd.read_excel('./scrape_new_data/notable_schools_org_data.xlsx')
    english_cols = ['School Title', 'Cluster', 'Management', 'Building', 'Drinking Water', 'Wall', 'nearby_schools', 'Village / Town',
                    'District', 'Block', 'Instruction Medium', 'Board for Class 10th', 'Board for Class 10+2', 'Residential Type', 'Head Teacher']
    cols_list, data = ['School Code'], []
    for col in english_cols:
        cols_list.append(col)
        cols_list.append(col + '_Telugu')
    part_num = int(sys.argv[1])
    start_idx = part_num * CHUNK_SIZE
    a = a[start_idx:start_idx + CHUNK_SIZE]
    for i, row in a.iterrows():
        t = time.time()
        curr_row = get_translated_data(row)
        data.append(curr_row)
        curr_t = time.time()
        print(f'{i} schools done. Time taken for school {i} = {curr_t - t} secs')
    df = pd.DataFrame(data, columns=cols_list)
    df.to_excel(f'./scrape_new_data/translated_dataset_notable_schools_{part_num}.xlsx')
    
if __name__ == "__main__":
    main()