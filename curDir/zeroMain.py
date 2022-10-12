#1. Change global variables (global variable)
#2. Change the file being used for articleParts (articlePartsFile)
#3. Change the file for xml generation (fobj)
#4. Change the number of codes you want articles for (start; end)
#		name of csv will automatically change

#coding: utf-8
import os, re, sys, csv, json, string, pickle, random
import pandas as pd
from hashlib import sha1
from write import getWikiText
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from template_functions import *

## indicwiki's and tewiki's xml headers ##
indicwiki = '''<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="te">
	<siteinfo>
		<sitename>indicwiki</sitename>
		<dbname>indicwiki130920</dbname>
		<base>http://indicwiki.iiit.ac.in/index.php/%E0%B0%AE%E0%B1%8A%E0%B0%A6%E0%B0%9F%E0%B0%BF_%E0%B0%AA%E0%B1%87%E0%B0%9C%E0%B1%80</base>
		<generator>MediaWiki 1.34.0</generator>
		<case>first-letter</case>
		<namespaces>
			<namespace key="-2" case="first-letter">మీడియా</namespace>
			<namespace key="-1" case="first-letter">ప్రత్యేక</namespace>
			<namespace key="0" case="first-letter" />
			<namespace key="1" case="first-letter">చర్చ</namespace>
			<namespace key="2" case="first-letter">వాడుకరి</namespace>
			<namespace key="3" case="first-letter">వాడుకరి చర్చ</namespace>
			<namespace key="4" case="first-letter">Project</namespace>
			<namespace key="5" case="first-letter">Project చర్చ</namespace>
			<namespace key="6" case="first-letter">దస్త్రం</namespace>
			<namespace key="7" case="first-letter">దస్త్రంపై చర్చ</namespace>
			<namespace key="8" case="first-letter">మీడియావికీ</namespace>
			<namespace key="9" case="first-letter">మీడియావికీ చర్చ</namespace>
			<namespace key="10" case="first-letter">మూస</namespace>
			<namespace key="11" case="first-letter">మూస చర్చ</namespace>
			<namespace key="12" case="first-letter">సహాయం</namespace>
			<namespace key="13" case="first-letter">సహాయం చర్చ</namespace>
			<namespace key="14" case="first-letter">వర్గం</namespace>
			<namespace key="15" case="first-letter">వర్గం చర్చ</namespace>
			<namespace key="828" case="first-letter">మాడ్యూల్</namespace>
			<namespace key="829" case="first-letter">మాడ్యూల్ చర్చ</namespace>
			<namespace key="2300" case="first-letter">Gadget</namespace>
			<namespace key="2301" case="first-letter">Gadget talk</namespace>
			<namespace key="2302" case="case-sensitive">Gadget definition</namespace>
			<namespace key="2303" case="case-sensitive">Gadget definition talk</namespace>
			<namespace key="2600" case="first-letter">Topic</namespace>
		</namespaces>
	</siteinfo>\n'''

tewiki = '''<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="te">
	<siteinfo>
		<sitename>tewiki</sitename>
		<dbname>indicwiki</dbname>
		<base>https://tewiki.iiit.ac.in/index.php?title=%E0%B0%AE%E0%B1%8A%E0%B0%A6%E0%B0%9F%E0%B0%BF_%E0%B0%AA%E0%B1%87%E0%B0%9C%E0%B1%80</base>
		<generator>MediaWiki 1.34.0</generator>
		<case>first-letter</case>
		<namespaces>
			<namespace key="-2" case="first-letter">మీడియా</namespace>
			<namespace key="-1" case="first-letter">ప్రత్యేక</namespace>
			<namespace key="0" case="first-letter" />
			<namespace key="1" case="first-letter">చర్చ</namespace>
			<namespace key="2" case="first-letter">వాడుకరి</namespace>
			<namespace key="3" case="first-letter">వాడుకరి చర్చ</namespace>
			<namespace key="4" case="first-letter">Project</namespace>
			<namespace key="5" case="first-letter">Project చర్చ</namespace>
			<namespace key="6" case="first-letter">దస్త్రం</namespace>
			<namespace key="7" case="first-letter">దస్త్రంపై చర్చ</namespace>
			<namespace key="8" case="first-letter">మీడియావికీ</namespace>
			<namespace key="9" case="first-letter">మీడియావికీ చర్చ</namespace>
			<namespace key="10" case="first-letter">మూస</namespace>
			<namespace key="11" case="first-letter">మూస చర్చ</namespace>
			<namespace key="12" case="first-letter">సహాయం</namespace>
			<namespace key="13" case="first-letter">సహాయం చర్చ</namespace>
			<namespace key="14" case="first-letter">వర్గం</namespace>
			<namespace key="15" case="first-letter">వర్గం చర్చ</namespace>
			<namespace key="120" case="first-letter">Item</namespace>
			<namespace key="121" case="first-letter">Item talk</namespace>
			<namespace key="122" case="first-letter">Property</namespace>
			<namespace key="123" case="first-letter">Property talk</namespace>
			<namespace key="482" case="first-letter">Config</namespace>
			<namespace key="483" case="first-letter">Config talk</namespace>
			<namespace key="710" case="first-letter">TimedText</namespace>
			<namespace key="711" case="first-letter">TimedText talk</namespace>
			<namespace key="828" case="first-letter">మాడ్యూల్</namespace>
			<namespace key="829" case="first-letter">మాడ్యూల్ చర్చ</namespace>
			<namespace key="2300" case="first-letter">Gadget</namespace>
			<namespace key="2301" case="first-letter">Gadget talk</namespace>
			<namespace key="2302" case="case-sensitive">Gadget definition</namespace>
			<namespace key="2303" case="case-sensitive">Gadget definition talk</namespace>
			<namespace key="2600" case="first-letter">Topic</namespace>
			<namespace key="3022" case="first-letter">Tewiki</namespace>
			<namespace key="3023" case="first-letter">Tewiki talk</namespace>
		</namespaces>
	</siteinfo>\n'''
## Change above values if different website is picked ##

## Change the below global variables ##
page_id =300000

user_id ="57"
username ="TeWikiSchoolBot"

dataFolder ='./data/'
destinationFolder = './data/trials/'

# articlePartsFile = 'sample.pkl'

# Map that determines the order of parts in the article # Default Order: 'abcdefghijklmnopq'
# orderMap ={'a': 'Location', 'b': 'Details', 'c': 'Academics', 'd': 'Counts',
# 				'e': 'Ending', 'f': 'References', 'g': 'Facilities', 'h': 'Extracurricular',
# 				'i': 'Admissions', 'j': 'Faculty', 'k': 'History', 'l': 'Achievements'}

## Global Variables Above ## 

## Functions to format and write xml data to file
def sha36(page_id):
	page_id = str(page_id).encode('utf-8')
	sha16 =sha1(page_id).hexdigest()
	sha10 =int(sha16, 16)

	chars =[]
	alphabets = string.digits +string.ascii_lowercase
	while sha10>0:
		sha10, r = divmod(sha10, 36)
		chars.append(alphabets[r])
	
	return ''.join(reversed(chars))

# Loads the final dataset comprising all schools
def load_all_schools_df():
    conc = pd.DataFrame()
    for j in range(1, 4):
        with open(f'./scrape_new_data/schools_org_data_part_{j}.pkl', 'rb') as f:
            a = pickle.load(f)
            conc = pd.concat([conc, a], axis=0)
    return conc

# Incorportate translated titles into dataset
def include_translated_titles():
    a = pd.DataFrame()
    with open(f'./scrape_new_data/notable_schools_org_data.pkl', 'rb') as f:
        a = pickle.load(f)
    print(a.shape)
    titles = pd.read_csv('./scrape_new_data/School-titles.csv')
    titles['School Code'] = titles['School Code'].astype(int)
    titles.drop(columns=['Unnamed: 0'], inplace=True)
    a = pd.merge(left=a, right=titles, how="left", on="School Code")
    a = a.drop_duplicates('School Code')
    with open(f'./scrape_new_data/notable_schools_org_data.pkl', 'wb') as f:
        print(a.shape)
        pickle.dump(a, f)  

# Loads the dataset corresponding to notable schools
def load_notable_schools_df():
    a = pd.DataFrame()
    with open(f'./scrape_new_data/notable_schools_org_data.pkl', 'rb') as f:
        a = pickle.load(f)
    print(a.shape)
    b = {}
    with open(f'./scrape_new_data/school_urls_dict.pkl', 'rb') as f:
        b = pickle.load(f)
    return a, b

# Function to replace possible special characters
def clean(text, isTitle):
    cleaned_text = text.replace('&',"&amp;").replace('<',"&lt;").replace('>',"&gt;").replace('"',"&quot;").replace("'","&apos;").replace("^", "&circ;").replace('~', '&tilde;')
    if not isTitle:
        return cleaned_text
    return cleaned_text.replace('_'," ")

def writePage(title, wikiText, fobj):
	global user_id, username

	pglen = len(wikiText)
	time =datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
	
	curPage ='''\n\n
	<page>
		<title>''' +clean(title, True) +'''</title>
		<ns>0</ns>
		<id>''' +str(page_id) +'''</id>
		<revision>
			<id>''' +str(page_id) +'''</id>
			<timestamp>'''+time+'''</timestamp>
			<contributor>
				<username>''' +username +'''</username>
				<id>''' +str(user_id) +'''</id>
			</contributor>
			<comment>xmlpage created</comment>
			<model>wikitext</model>
			<format>text/x-wiki</format>
			<text xml:space="preserve" bytes="''' +str(pglen) +'''">''' +clean(wikiText, False) +'''
			</text>
			<sha1>''' +sha36(page_id) +'''</sha1>
		</revision>
	</page>
	\n\n'''

	fobj.write(curPage)
	return

# Outdated code: Shows the columns of ArticleParts' Details (default columns)
# ## Funtions to create a new DF
# def newDF():
# 	df =pd.DataFrame(columns=['PageID', 'Code', 'Title', 'Infobox', 'Location', 'Details', 
# 											'Academics', 'Counts', 'Ending', 'References', 'Facilities', 
# 											'Extracurricular', 'Admissions', 'Faculty', 'History', 'Achievements', 'Order'])

# 	return df

#This writes articles and then creates a dataframe based on it 
#also formats the same as XML data and write it to a file
def generateXmlAndSaveDF(wikiSiteInfo, textTemplate, startIndex=int(sys.argv[1]), endIndex=int(sys.argv[2])):
	# Load Data
	global dataFolder, page_id
	# School Data and the ready codes
	oneKB, urls_dict = load_notable_schools_df()
	# codes =pickle.load(open(dataFolder+'readyCodes.pkl', 'rb'))

	# Get list of codes to generate articles for
	start = startIndex; end = endIndex
	# codes = oneKB['School Code'].astype(int).tolist()
	with open('./scrape_new_data/important_schools.json', 'r') as _f:
		codes = json.load(_f)
	# codes = codes[start:end]
	# codes = [28204401308]
	# row with most non-nulls - id:1000
	# codes = [36092600625] * 1
	# notable schools diverse codes below - id:2000
	# codes = [36011503203, 36095190748, 36093400204, 36090301120, 36095190923, 36091801140, 36091201202, 36091201303, 36091201608, 36091201629, 36091201502, 36091201804, 36095190859, 36091200810, 36095190221, 36093901829, 36091801119, 36074500110, 36092600625]
	# overall diverse codes below
	# codes = [28150702403, 28152702205, 28132991224, 28150800720, 28152891108, 28151890852, 28151800909, 28151800602, 28152891111, 28154000849, 36094901603, 36094903204, 36091401902, 36095190241, 36095190908, 36091201625, 36091201303, 36091201608, 36091201624, 36091201804, 36091201604, 36095190221, 36091801119, 36092600625]
	# # codes =random.sample(codes, 10)
	# codes = [28163100119, 28140100401, 28140100910, 28140103501, 28140104904, 28140309802, 28140800908, 28140800916, 28141700212, 28142190763, 28142990322, 28171590918, 28172600603, 28172500310, 28143500306, 28175201713]
	# codes = map(str, codes)
	#File names:
	articlePartsFile ='articleParts'+str(start)+'-'+str(end)+'.csv'
	onePageFile ='onePage'+str(start)+'-'+str(end)+'.xml'
	titlesFile ='title'+str(start)+'-'+str(end)+'.csv'
	errFile ='error'+str(start)+'-'+str(end)+'.txt'

	#1. Intermediate Steps saved as csv
	fobj =open(destinationFolder+articlePartsFile, 'w')
	articleParts = csv.DictWriter(fobj, fieldnames=['Code', 'Details'])

	#2. Final XML page which is to be uploaded in mediawiki
	fobj = open(destinationFolder+onePageFile, "w")
	fobj.write(wikiSiteInfo+'\n')

	#3. Creates a csv file for titles to be corrected later 
	titleWriter = csv.writer(open(destinationFolder+titlesFile, 'w'))
	titleWriter.writerow(['UDISE Code', 'English Title', 'Telugu Title'])

	#4. Errors log
	errObj =open(destinationFolder+errFile, 'w')

	for i, code in enumerate(codes):
		# try:
		start = datetime.now()
		current_df = oneKB.loc[oneKB['School Code']==code]
		title, wikiText = '', ''
		for idx, row in current_df.iterrows():
			# print(row['School Title_Telugu'])
			# print(row['telugu_corrected_title'])
			if not (row['telugu_corrected_title'] == None or pd.isnull(row['telugu_corrected_title']) or str(row['telugu_corrected_title']) == ''):
				row['School Title_Telugu'] = row['telugu_corrected_title']
			title, wikiText = getWikiText(row, textTemplate, urls_dict[str(row['School Code'])])
			#Write row to csv file
			titleWriter.writerow([code, row['School Title'].strip(), title])
		# Save intermediate representation to a dataframe, ArticleParts
		parts = tuple([p.strip(' \n\t\r') for p in wikiText.split('<$>')])
		Overview, Details, Academics, Counts, Infrastructure, References, Infobox = parts
		if len(Counts) > 0:
			Counts = '\n===బోధనా సిబ్బంది===\n' + Counts
		if len(Infrastructure) > 0:
			Infrastructure = '\n===మౌలిక సదుపాయాలు===\n' + Infrastructure
		if len(Academics) > 0:
			Academics = '\n==విద్యాలయ వివరాలు==\n' + Academics
		
		details =json.dumps({'PageID':page_id, 'Code':code, 'Title':title.strip(), 'Infobox':Infobox, 'Overview':Overview, 
					'Details':Details, 'Counts':Counts, 'References':References, 'Academics': Academics, 'Infrastructure': Infrastructure, 'Facilities':'', 'Extracurricular':'', 
     				'Admissions':'', 'Faculty':'', 'History':'', 'Achievements':'', 'Order':'abcdefghijkl'})		

		articleParts.writerow({'Code':code, 'Details':details})
		
		# Format and write the wikitext to an XML file
		s = '\n\n'
		wikiText = Infobox + s + Overview + s + Details + s + Academics + s + Counts + s + Infrastructure + s + References
		wikiText = wikiText.strip(' \n\t\r')
		writePage(f'{title}', wikiText, fobj)

		# Performance check
		end = datetime.now()
		diff = str((end-start).seconds)+':'+str((end-start).microseconds)[:3]
		print(startIndex+i,':',code,'-', title, '\t time taken:', diff)

		page_id +=1
		# except:
		# 	print('#Failed @', startIndex+i, ':', code)
		# 	errObj.write(str(code)+'\n')

	print("stopped before",page_id)
	fobj.write('\n</mediawiki>\n')

	fobj.close()
	errObj.close()

def main():
	# Load school's templates
	file_loader = FileSystemLoader('template')
	env = Environment(loader=file_loader)

	dfTextTemplate =env.get_template('final_teluguDFtext.j2')
	functions_dict = {
        "is_valid": is_valid,
        "get_intro_line_1": get_intro_line_1,
        "get_intro_line_2": get_intro_line_2,
        "get_intro_line_3": get_intro_line_3,
        "get_intro_line_4": get_intro_line_4,
        "get_class_info": get_class_info,
        "get_teacher_info": get_teacher_info,
        "get_students_info": get_students_info,
        "get_gender_info": get_gender_info,
        "get_management_area_info": get_management_area_info,
        "get_nearby_schools": get_nearby_schools,
        "get_board_info": get_board_info,
        "get_residential_details": get_residential_details,
        "get_pre_primary_teachers_info": get_pre_primary_teachers_info,
        "get_head_teachers_info": get_head_teachers_info,
        "get_building_and_class_rooms_info": get_building_and_class_rooms_info,
        "_t": "_t",
        "get_toilet_info": get_toilet_info,
        "get_electricity_water_info": get_electricity_water_info,
        "get_wall_info": get_wall_info,
        "get_ramps_info": get_ramps_info,
        "get_library_and_books_info": get_library_and_books_info,
        "get_playground_info": get_playground_info,
        "get_computers_info": get_computers_info
    }
	dfTextTemplate.globals.update(functions_dict)
	print(sys.argv)

	# Generate Dataframe
	# Columns: [PageID, Code, Title, Infobox, Location, Details, Academics, Counts, 
	#				Ending, References, Facilities, Extracurricular, Admissions, Faculty, 
	#				History, Achievements, Order]
	# generateXmlAndSaveDF(tewiki, dfTextTemplate, 0, 9754)
	# generateXmlAndSaveDF(tewiki, dfTextTemplate, 21055, 21060)

	generateXmlAndSaveDF(tewiki, dfTextTemplate)


if __name__ == "__main__":
	# 'articleParts.pkl' is the name of the dataframe, in the data folder
	main() #This generates a dataframe and saves it as articleParts.pkl