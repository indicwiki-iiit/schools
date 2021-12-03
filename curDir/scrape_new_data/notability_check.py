# Helper file to find non-sparse and sparse rows, and make various notability checks
import pandas as pd
import re
import pickle
from collections import OrderedDict

# Checks if an attribute value is valid
def is_valid(value):
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, bool):
        return value
    if (value == None) or (pd.isnull(value)) or \
    (str(value) in ["[]", '', "None", 'none', 'N/A', 'n/a', 'Not Applicable', 'not applicable', 'nan', 
                    'Others', 'others', 'No Boundary Wall', 'no boundary wall', 'No Building', 'no building',
                    'Unrecognised', 'unrecognised']):
        return False
    if isinstance(value, float) or isinstance(value, int):
        return value > 0 and str(value) != 'nan'
    return not value in ['', 'nan', '-1']

# Obtains stripped value for attribute
def get_stripped_val(val):
    if not is_valid(val):
        return val
    val2 = val
    if isinstance(val, float):
        val2 = int(val)
    val3 = str(val2)
    return val3.strip()

# Obtains stripped and lower case values for attribute
def get_stripped_lower_val(val):
    if not is_valid(val):
        return val
    val2 = val
    if isinstance(val, float):
        val2 = int(val)
    val3 = str(val2)
    return val3.strip().lower()

# converts to int
def get_int(value):
    if not is_valid(value):
        return -1
    return int(value)

# with open('./notable_schools_org_data.pkl', 'rb') as f:
#     a = pickle.load(f)
# all_attributes = a.columns.tolist()

a = pd.read_excel('schools_org_data.xlsx')
all_attributes = a.columns.tolist()
ctr = 0
TEACHER_COUNT_THRESHOLD = 6
CLASS_ROOMS_THRESHOLD = 3
BOYS_TOILETS_THRESHOLD = 1
GIRLS_TOILETS_THRESHOLD = 1
NON_NULLS_THRESHOLD = 15
notable_schools = []

for i, row in a.iterrows():
    val1 = get_int(row['Female Teacher'])
    val2 = get_int(row['Male Teachers'])
    val = val1 + val2
    if val1 == -1 or val2 == -1:
        continue
    if val < TEACHER_COUNT_THRESHOLD:
        continue
    if get_int(get_stripped_lower_val(row['Class Rooms'])) < CLASS_ROOMS_THRESHOLD:
        continue
    if get_int(get_stripped_lower_val(row['Boys Toilet'])) < BOYS_TOILETS_THRESHOLD:
        continue
    if get_int(get_stripped_lower_val(row['Girls Toilet'])) < GIRLS_TOILETS_THRESHOLD:
        continue
    non_nulls_count = 0
    for attribute in all_attributes:
        if not is_valid(row[attribute]):
            continue
        non_nulls_count += 1
    if non_nulls_count < NON_NULLS_THRESHOLD:
        continue
    current_row = []
    for attribute in all_attributes:
        current_row.append(row[attribute])
    notable_schools.append(current_row)
    ctr += 1
print(ctr)

notable_schools_df = pd.DataFrame(notable_schools, columns = all_attributes)
print(notable_schools_df.shape)
notable_schools_df.to_excel('./notable_schools_org_data.xlsx')
with open('./notable_schools_org_data.pkl', 'wb') as f:
    pickle.dump(notable_schools_df, f)

# Below code corresponds to finding out articles (rows) with different non-null attribute counts

diverse_codes_list, diverse_codes = [], OrderedDict()
req_list = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
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
