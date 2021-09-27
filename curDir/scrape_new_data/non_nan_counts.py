# Helper fine to find non-sparse and sparse rows
import pandas as pd
import re
from collections import OrderedDict

# Checks if an attribute value is valid
def is_valid(value):
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, bool):
        return value
    if (value == None) or (pd.isnull(value)) or (str(value) in ["[]", '', "None", 'N/A', 'n/a', 'Not Applicable', 'nan']):
        return False
    if isinstance(value, float) or isinstance(value, int):
        return value > 0 and str(value) != 'nan'
    return not value in ['', 'nan', '-1']

a = pd.read_excel('schools_org_data.xlsx')
all_attributes = a.columns.tolist()
diverse_codes_list, diverse_codes = [], OrderedDict()
req_list = [1, 6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
for i, row in a.iterrows():
    ctr = 0
    for attribute in all_attributes:
        if not is_valid(row[attribute]):
            continue
        ctr += 1
    diverse_codes[ctr] = row['School Code']
diverse_codes = OrderedDict(sorted(diverse_codes.items(), key=lambda s: s[0]))
for _k, _v in diverse_codes.items():
    diverse_codes_list.append(_v)
with open('diverse_schools_list.txt', 'w') as f:
    f.write(str(diverse_codes_list))
