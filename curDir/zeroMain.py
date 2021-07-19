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
		<base>https://tewiki.iiit.ac.in/index.php/%E0%B0%AE%E0%B1%8A%E0%B0%A6%E0%B0%9F%E0%B0%BF_%E0%B0%AA%E0%B1%87%E0%B0%9C%E0%B1%80</base>
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
## Change above values if different website is picked ##

## Change the below global variables ##
page_id =300000

user_id ="57"
username ="TeWikiSchoolBot"

dataFolder ='./data/'
destinationFolder = './data/epoch/'

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

def writePage(title, wikiText, fobj):
	global user_id, username

	pglen = len(wikiText)
	time =datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
	
	curPage ='''\n\n
	<page>
		<title>''' +title +'''</title>
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
			<text xml:space="preserve" bytes="''' +str(pglen) +'''">
			\n''' +wikiText +'''
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
	oneKB =pickle.load(open(dataFolder+'oneKB.pkl', 'rb'))
	codes =pickle.load(open(dataFolder+'readyCodes.pkl', 'rb'))

	# Get list of codes to generate articles for
	start = startIndex; end = endIndex
	# codes =codes[start:end]
	codes = [28204401308]
	# # codes =random.sample(codes, 10)

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
		details =oneKB.loc[oneKB['School Code']==code].values.tolist()[0]
		title, wikiText=getWikiText(details, textTemplate)
		
		#Write row to csv file
		titleWriter.writerow([code, details[4].strip(), title])

		# Save intermediate representation to a dataframe, ArticleParts
		parts =wikiText.split('<$>')
		
		Infobox, Location, Details, Academics, Counts, Ending, References = parts[6], parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
		
		details =json.dumps({'PageID':page_id, 'Code':code, 'Title':title.strip(), 'Infobox':Infobox.strip(), 'Location':Location.strip(), 
					'Details':Details.strip(), 'Academics':Academics.strip(), 'Counts':Counts.strip(), 'Ending':Ending.strip(),
					'References':References.strip(), 'Facilities':'', 'Extracurricular':'', 'Admissions':'', 'Faculty':'', 'History':'',
					'Achievements':'', 'Order':'abcdefghijkl'})

		articleParts.writerow({'Code':code, 'Details':details})
		
		# Format and write the wikitext to an XML file
		wikiText =Infobox.strip()+'\n '+Location.strip()+' '+Details.strip()+' '+Academics.strip()+' '+Counts.strip()+' '+Ending.strip()+'\n\n'+References.strip()
		writePage(title, wikiText, fobj)

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

	dfTextTemplate =env.get_template('teluguDFtext.j2')

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