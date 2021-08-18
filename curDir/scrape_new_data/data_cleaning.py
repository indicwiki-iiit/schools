# Generates sweetviz report and has some basic data cleaning
import pandas as pd
import sweetviz as sv
import pickle

# Loads the final dataset
def load_df():
    conc = pd.DataFrame()
    for j in range(1, 4):
        with open(f'./schools_org_data_part_{j}.pkl', 'rb') as f:
            a = pickle.load(f)
            conc = pd.concat([conc, a], axis=0)
    return conc

# Handles missing values to ensure uniformity
def validate_value(attribute_value):
    if attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) in ["[]", '', "None", 'Not Applicable', 'nan']:
        if isinstance(attribute_value, float):
            return None
        return 'nan'
    return attribute_value

def main():
    df = load_df()
    df.drop(columns=['Contract Teachers'], inplace=True)
    for i, row in df.iterrows():
        for c in df.columns.tolist():
            row[c] = validate_value(row[c])
    dfs = [pd.DataFrame(), df[:50000], df[50000:100000], df[100000:]]
    for j in range(1, 4):
        with open(f'schools_org_data_part_{j}.pkl', 'wb') as f:
            pickle.dump(dfs[j], f)
    df.to_excel('schools_org_data.xlsx', index=False)
    
if __name__ == '__main__':
	main()