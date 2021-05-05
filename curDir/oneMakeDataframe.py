#coding: utf-8
import re
import pickle
import pandas as pd
from write import getWikiText
from jinja2 import Environment, FileSystemLoader

## Change the below global variables ##
page_id =300001

user_id ="57"
username ="Harshapamidipalli"

dataFolder ='./data/'
## Global Variables Below ## 

def newDF():
	df =pd.DataFrame(columns=['PageID', 'Code', 'Title', 'Infobox', 'Location', 'Details', 
											'Academics', 'Counts', 'Ending', 'References', 'Facilities', 
											'Extracurricular', 'Admissions', 'Faculty', 'History', 'Achievements', 'Order'])

	return df

#This writes articles and then creates a dataframe based on it
def dataframeGenerator(titleTemplate, textTemplate):
	# Load Data
	global dataFolder
	
	oneKB =pickle.load(open(dataFolder+'oneKB.pkl', 'rb'))
	
	articleParts =newDF()
	# Comment the below line if you want to reset articleParts
	# articleParts =pickle.load(open(dataFolder+'articleParts.pkl', 'rb'))

	# Map that determines the order of parts in the article
	orderMap ={'a': 'Location', 'b': 'Details', 'c': 'Academics', 'd': 'Counts',
					'e': 'Ending', 'f': 'References', 'g': 'Facilities', 'h': 'Extracurricular',
					'i': 'Admissions', 'j': 'Faculty', 'k': 'History', 'l': 'Achievements'}
	# Default Order: 'abcdefghijklmnopq'

	##################
	### For Multiple codes ###
	##################
	# codes =oneKB['School Code'].tolist()
	# # codes =random.sample(codes, 10)
	codes = [28162400403, 28204700620, 28210800903, 28203190221, 28142801102, 
				28140307302, 28212800505, 28144000805, 28173301206, 28161790898]
	# codes = [28162400403]

	global page_id
	for code in codes:
		print(code)
		details =oneKB.loc[oneKB['School Code']==code].values.tolist()[0]
		title, wikiText=getWikiText(details, titleTemplate, textTemplate)
		
		parts =wikiText.split('\n<$>')
		newRow ={'PageID':page_id, 'Code':code, 'Title':title.strip(), 'Infobox':parts[0], 'Location':parts[1], 
					'Details':parts[2], 'Academics':parts[3], 'Counts':parts[4], 'Ending':parts[5],
					'References':parts[6], 'Facilities':'', 'Extracurricular':'', 'Admissions':'', 'Faculty':'', 'History':'',
					'Achievements':'', 'Order':'abcdefghijkl'}

		articleParts =articleParts.append(newRow, ignore_index=True)

		page_id +=1

	print("stopped before",page_id)

	pickle.dump(articleParts, open(dataFolder+'articleParts.pkl', 'wb'))


def main():
	# Load school's templates
	file_loader = FileSystemLoader('template')
	env = Environment(loader=file_loader)

	titleTemplate = env.get_template('teluguTitle.j2')
	dfTextTemplate =env.get_template('teluguDFtext.j2')

	# Generate Dataframe
	dataframeGenerator(titleTemplate, dfTextTemplate)
	# Columns: [PageID, Code, Title, Infobox, Location, Details, Academics, Counts, 
	#				Ending, References, Facilities, Extracurricular, Admissions, Faculty, 
	#				History, Achievements, Order]


if __name__ == "__main__":
	# 'articleParts.pkl' is the name of the dataframe, in the data folder
	main() #This generates a dataframe and saves it as articleParts.pkl