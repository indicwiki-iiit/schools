#coding: utf-8
import re
import string
import pickle
import random
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
page_id =300001

user_id ="57"
username ="Harshapamidipalli"
## Change the above global variables ##

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

def addPage(title, wikiText, pages):
	global user_id, username

	pglen = len(wikiText)
	time =datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
	
	pages = pages +'''\n\n
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

	return pages

#This writes articles and then generates an xml page which 
#can be directly imported in mediawiki (tewiki)
def xmlGenerator(wikiSiteInfo, titleTemplate, textTemplate, oneKB):
	codes =oneKB['School Code'].tolist()
	codes =random.sample(codes, 3)
	print(len(codes), codes)
	# Generate XML Page
	pages = ""
	global page_id
	for code in codes:
		print(code)
		details =oneKB.loc[oneKB['School Code']==code].values.tolist()[0]
		title, wikiText=getWikiText(details, titleTemplate, textTemplate)
		print('\t', title)
		pages = addPage(title, wikiText, pages)
		page_id +=1

	xmlpage = wikiSiteInfo +pages +'</metadata>'
	fobj = open("autoXml22k.xml", "w")
	fobj.write(xmlpage)
	fobj.close()

	print("stopped before",page_id)

def main():
	# Load school's templates
	file_loader = FileSystemLoader('template')
	env = Environment(loader=file_loader)
	titleTemplate = env.get_template('teluguTitle.j2')
	dfTextTemplate =env.get_template('teluguDFtext.j2')
	xmlTextTemplate = env.get_template('teluguXMLtext.j2')

	# Load school's data
	oneKB =pickle.load(open('./data/oneKB.pkl', 'rb'))

	# Generate xml 
	xmlGenerator(tewiki, titleTemplate, xmlTextTemplate, oneKB)
	
if __name__ == "__main__":
	main() #This writes articles to xmlpages