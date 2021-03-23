# Unifies all dataframes of school data extracted from excel sheet
# dataframes (one per district)

import os
import pickle
import pandas as pd

DB_dir = './excelDB_pkls'

def main():
	districts =pickle.load(open(DB_dir+'/DISTRICTS', 'rb')) #DISTRICTS is a pickle containing a list of all districts in the folder
	first =True
	oneDF =None

	for dist in districts:
		print(dist)
		dist_df =pickle.load(open(DB_dir+'/'+dist, 'rb'))
		if first:
			first =False
			halfDF = dist_df
		else:
			oneDF =pd.concat([halfDF, dist_df])

		print("   ", oneDF.shape)

	pickle.dump(halfDF, open('halfDF.pkl', 'wb'))

if __name__ == '__main__':
	main()