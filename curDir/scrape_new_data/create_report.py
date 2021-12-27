import pandas as pd
import pickle
import sweetviz as sv

a = pd.DataFrame()
with open(f'./notable_schools_org_data.pkl', 'rb') as f:
    a = pickle.load(f)
print(a.shape)
a = a.astype(str)
report = sv.analyze(a, pairwise_analysis='off')
report.show_html()