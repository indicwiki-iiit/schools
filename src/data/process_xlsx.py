# Reads scraped excel sheet (one per district) 
# Cleans and normalises it
# Creates a Unified dataframe and stores it as a pickle

import os
import pickle
import pandas as pd

source_dir = './scraped_xlsx/'

# Dataframe of List of school details that have to be manually checked
errors =pd.DataFrame()

# Unified Dataframe for all scraped data
newlyScraped =pd.DataFrame()

# Dictionary to normalise School Category values
category_code = {'Upper Pri.+ Sec. And H.Sec.':'UP.S.HS', 'H.Sec.only/Jr.College':'HS', 'Pri. + U.Pri. + Sec. And H.Sec.':'P.UP.S.HS', 'Upper Primary And Secondary':'UP.S', 'Upper Primary only':'UP', 'Primary Only':'P', 'Secondary with H.Sec.':'S.HS', 'Pri. + U.Pri And Secondary':'P.UP.S', 'Secondary only':'S', 'Primary with U.Primary':'P.UP'}

# Clean and Check df
# Concatinate with newlyScraped
def clean(df):
	global errors
	global newlyScraped

	df.reset_index(drop=True, inplace=True)

	errCodes =[]
	
	#Code to handle duplicate school rows
	if not df['School Code'].is_unique:
		codes =df['School Code']
		duplicates =codes[codes.duplicated(keep=False)]
		print(duplicates.shape[0], "duplicates found :(")
		return pd.Dataframe()

	# column numbers of the attributes in the df
	sCode=1; category=4; sType=7
	boys=8; girls=9; totalEnr=10
	male=11; female=12; teachers=13
	
	for i in range(df.shape[0]):
		check_needed = False
		code = df.iat[i, sCode]
		
		# Normalise school code
		cat =df.iat[i, category]
		try:
			df.iat[i, category] =category_code[cat]
		except:
			if cat not in category_code.values():
				print("Category", cat)
		
		# Make sure Total Teachers is not 0
		if df.iat[i, teachers] == 0:
			check_needed =True
		
		# Make sure School Type and enrolled students tally
		stype =df.iat[i, sType]
		bcnt =df.iat[i, boys];gcnt = df.iat[i, girls];total = df.iat[i, totalEnr]
		mcnt =df.iat[i, male];fcnt =df.iat[i, female];totalTeachers=df.iat[i, teachers]

		if bcnt+gcnt!=total or total==0:
			check_needed = True
		if mcnt+fcnt!=totalTeachers:
			check_needed = True
		if stype=='Boys' and gcnt>0:
			check_needed =True
		elif stype=='Girls' and bcnt>0:
			check_needed =True
		
		# Add code to errCodes if check needed !
		if check_needed:
			errCodes.append(code)

	#Append new Errors to errors (dataframe)	
	newErrors = df.loc[df['School Code'].isin(errCodes)]
	errors =pd.concat([errors, newErrors])
	#Delet new errors from df 
	rows =df[df['School Code'].isin(errCodes)].index
	df.drop(rows, inplace=True)

	return df


# Optimize HERE
# Clean and Check df
# Concatinate with newlyScraped
def clean2(df):
	global errors
	global newlyScraped
	global manual_check


# Finds inner join between halfDB and newlyScraped (based on the column "school's udise code") and returns
def updateKB():
	global newlyScraped
	halfDB =pickle.load(open("halfDB.pkl", 'rb'))

	newKB =pd.merge(halfDB, newlyScraped, how="inner", 
								left_on='udise_sch_code', right_on='School Code')


	return newKB

# Iterates through each new scraped excel sheet 
# Cleans and concatinates it to newlyScraped dataframe
def main():
	global errors
	global newlyScraped
	global manual_check

	files =os.listdir(source_dir)
	print(files)

	oldErrorCount = 0
	oldScrapeCount =0
	for file in files:
		df =pd.read_excel(source_dir+file) #df -> panda's DataFrame
		
		print(file, "Before cleaning shape:", df.shape)
		newlyScraped =pd.concat([newlyScraped, clean(df)])

		print("\t errors: +"+str(errors.shape[0]-oldErrorCount))
		print("\t scraped: +"+str(newlyScraped.shape[0]-oldScrapeCount))
		
		oldErrorCount = errors.shape[0]
		oldScrapeCount =newlyScraped.shape[0]

	print("newlyScraped:", newlyScraped.shape, "| errors:", errors.shape)

	#Check if oneKB.pkl already exists. If yes, concatinate newKB (merge between halfDB and newlyScraped) with oneKB
	#else oneKB = newKB
	newKB =updateKB()
	try:
		a =asdfasdf
		oneKB =pickle.load(open('oneKB.pkl', 'rb'))
		oneKB =pd.concat([oneKB, newKB])
	except:
		oneKB =newKB

	oneKB =oneKB[[	'DISTNAME', 'BLKNAME', 'VILNAME', 'School Code', 'School Name', 'SCHCAT_DESC', 
							'SCHMGT_DESC', 'Medium', 'School Category', 'School Type', 'Rural Urban', 
							'Enr Boys', 'Enr Girls', 'Total Enr', 'Male Teacher', 'Female Teacher', 'Total Teacher'
						]]

	#Check if allScraped.pkl already exists. if yes, concatinate newlyScraped with allScraped, 
	#else allScraped = newlyScraped 
	try:
		a =sdfsdaf
		allScraped =pickle.load(open('allScraped.pkl', 'rb'))
		allScraped =pd.concat([allScraped, newlyScraped])
	except:
		allScraped =newlyScraped

	# DUMP ALL DATA !
	pickle.dump(oneKB, open('oneKB.pkl', 'wb'))
	pickle.dump(allScraped, open('allScraped.pkl', 'wb'))

	pickle.dump(errors, open('errors.pkl', 'wb'))
	
	print("All excel sheets porcessed, please move all the files from ", source_dir, " to ./processed_xlsx/ !")

if __name__ == '__main__':
	main()