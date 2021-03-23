import string
from hashlib import sha1

from gen import write
from help import getData
from datetime import datetime
from xmlTemplate import tewiki

## Change the below global variables ##
page_id =300000

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

def addPage(title, article, pages):
	pglen = len(article)
 
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
			\n''' +article +'''
			</text>
			<sha1>''' +sha36(page_id) +'''</sha1>
		</revision>
	</page>
	\n\n'''

	return pages

def main():
	dfile_head = "../DBpckls/"
	pfile_head = "../PDFpckls/"
	dist = "ANANTAPUR"
	data, df, Ids = getData(dfile_head+dist, pfile_head+dist)

	Ids = [28223701001, 28223701002, 28223701003, 28223701004, 28223701005, 28221800501, 28221800502, 28221800503, 28223701101, 28223701103, 28223701104, 28223701105, 28221800601, 28221800602, 28223701201]

	pages = ""
	global page_id
	for Id in Ids:
		print(Id)
		title, article=write(data, df, Id)
		pages = addPage(title, article, pages)
		page_id +=1

	xmlpage = tewiki +pages +'</metadata>'
	fobj = open("autoXml.xml", "w")
	fobj.write(xmlpage)
	fobj.close()

	print("stopped before",page_id)


if __name__ == "__main__":
	main()