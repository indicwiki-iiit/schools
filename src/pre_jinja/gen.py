#coding: utf-8

import re
import random
from trans import transtelugu
from help import getData, class_nums, numToTelugu

#Fetches data for a given school ID
def getInfo(data, df, Id):
	details = data.loc[data['udise_sch_code']==Id].values.tolist()[0]
	counts = df.loc[df['Code']==str(Id)].values.tolist()[0]
	
	return details, counts

#Returns School's Basic Information
def getIntro(details):
	code = str(details[3]).strip()
	village = transtelugu(details[2].strip(), 0)
	district = transtelugu(details[0].strip(), 0)
	block = transtelugu(details[1].strip(), 0)
	
	introOpts = ["ఈ పాఠశాల "+village+"గ్రామంలో ఉన్నది. ఈ గ్రామం "+district+"జిల్లాలో "+block+"పరిధి నందు ఉన్నది. ",
					  "ఈ పాఠశాల "+village+"గ్రామంలో ఉన్నది. "+district+"జిల్లా నందు "+block+"పరిధిలో ఈ గ్రామం ఉన్నది. ",
					  district+"జిల్లాలో "+block+"పరిధిలో "+village+"గ్రామం నందు ఈ పాఠశాల ఉన్నది. ",
					  "ఈ పాఠశాల "+district+"జిల్లాలో "+block+"పరిధిలో గల "+village+"గ్రామము నందు ఉన్నది. "
					]
	
	intro = random.choice(introOpts)
	intro = intro+"ఈ పాఠశాల యొక్క ఏకీకృత జిల్లా సమాచార విద్యా వ్యవస్థ ([http://udise.in/ U-DISE]) కోడ్ "+code+". "
	
	return intro

#Returns Student's Type and Count of Students
def getStudentStats(counts):
	stuType = counts[1].lower()
	bcount =numToTelugu(counts[2])
	gcount = numToTelugu(counts[3])
	total = numToTelugu(int(counts[2])+int(counts[3]))
	
	pick = 1
	
	if 'co' in stuType:
		opts1 =[ "ఇది ఒక బాల బాలికల పాఠశాల. " ]
		opts2 = ["ఇక్కడ "+bcount+"బాలురు "+gcount+"బాలికలు, మొత్తం "+total+"విద్యార్థులు చదువుతున్నారు. ",
					 "ఈ పాఠశాల లో మొత్తం "+total+"విద్యార్థులు చదువుతున్నారు. వీరిలో "+bcount+"బాలురు "+gcount+"బాలికలు ఉన్నారు. ",
					 "మొత్తం "+total+"విద్యార్థులలో "+bcount+"బాలురు "+gcount+"బాలికలు ఈ పాఠశాల లో చదువుతున్నారు. "
					]
		
	elif 'boy' in stuType:
		opts1 = ["ఇది ఒక బాలుర పాఠశాల. ",
					 "ఈ పాఠశాల లో బాలురకు మాత్రమే ప్రవేశం ఉన్నది. ",
					 "బాలురకు మాత్రమే ఈ పాఠశాల నందు ప్రవేశం ఉన్నది. "
					]
		opts2 = ["ఇక్కడ చదువుతున్న బాలుర సాంఖ్య "+numToTelugu(counts[2],0)+". ", # 0 signifies, pick only numbers normal numbers (end case)
					 "ఈ పాఠశాల లో "+bcount+"బాలురు చదువుతున్నారు. ",
					  bcount+"బాలురు ఈ పాఠశాల లో చదువుతున్నారు. "
					]
		
	elif 'girl' in stuType:
		opts1 = ["ఇది ఒక బాలికల పాఠశాల. ",
					 "ఈ పాఠశాల లో బాలికలకు మాత్రమే ప్రవేశం ఉన్నది. ",
					 "బాలికలకు మాత్రమే ఇక్కడ ప్రవేశం ఉన్నది. "
				  ]
		opts2 = ["ఇక్కడ చదువుతున్న బాలికల సాంఖ్య "+numToTelugu(counts[3],0)+". ",
					 "ఈ పాఠశాల లో "+gcount+"బాలికలు చదువుతున్నారు. ",
					  gcount+"బాలికలు ఇక్కడ చదువుతున్నారు. "
					]
	else:
		pick = 0
		
	if pick:
		line1 = random.choice(opts1)
		line2 = random.choice(opts2)
		studentStats =line1+line2
	else:
		studentStats = ''
		
	return studentStats

#Returns Teacher's Stats and Reference
def getTeacherStats(counts):
	mint = int(counts[5])
	fint =int(counts[6])
	mcount = numToTelugu(mint)
	fcount = numToTelugu(fint)
	
	# if only male OR female teachers.
	if mint>0 and fint==0:
		line ="ఇక్కడ "+mcount+"ఉపాధ్యాయులు ఉన్నారు, వీరిలో అందరూ  ఉపాధ్యాయులే. "
	elif fint>0 and mint==0:
		line ="ఇక్కడ "+fcount+"ఉపాధ్యాయులు ఉన్నారు, వీరిలో అందరూ ఉపాధ్యాయినులే. "
	
	#Ekopadhya school
	elif mint==1 and fint==0:
		line ="ఇది ఒక ఏకోపాధ్యాయ పాఠశాల. ఒక ఉపాధ్యాయుడు ఉన్నారు. "
	elif fint==1 and mint==0:
		line ="ఇది ఒక ఏకోపాధ్యాయ పాఠశాల. ఒక ఉపాధ్యాయిని ఉన్నారు. "
	
	else:
		total = numToTelugu(mint+fint)
		opts =["ఈ పాఠశాల లో "+mcount+"ఉపాధ్యాయులు "+fcount+"ఉపాధ్యాయినులే, మొత్తం "+total+"ఉపాధ్యాయులు ఉన్నారు. ",
				   "ఇక్కడ మొత్తం "+total+"ఉపాధ్యాయులు ఉన్నారు. వీరిలో "+mcount+"ఉపాధ్యాయులు "+fcount+"ఉపాధ్యాయినులు ఉన్నారు. ",
				   "మొత్తం "+total+"ఉపాధ్యాయులు "+mcount+"ఉపాధ్యాయులు "+fcount+"ఉపాధ్యాయినులు ఇక్కడ ఉన్నారు. "
				 ]
		line = random.choice(opts)
			
	return line

#Returns School's Management's Description / TItile from school's name
def getDesc(details):
	name =details[4].strip()
	mgnt =details[6].strip()

	phrase =""
	
	if "Pvt.Aided" in mgnt:
		phrase = "ప్రైవేటు ఎయిడెడ్ పాఠశాల"
	elif "Pvt.Unaided" in mgnt:
		phrase = "ప్రైవేటు పాఠశాల"

	elif "KGBV" in name:
		phrase = "కస్తూర్బా గాంధీ బాలికా విద్యాలయ (KGBV)"
	elif "MPPS" in name:
		phrase = "మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల (MPPS)"
	elif "MPUPS" in name:
		phrase = "మండల ప్రజా పరిషత్ ప్రాథమికోన్నత పాఠశాల (MPUPS)"
	elif "ZPPS" in name:
		phrase = "జిల్లా పరిషత్ ప్రాథమిక పాఠశాల (ZPPS)"
	elif "ZPHS" in name:
		phrase = "జిల్లా పరిషత్ ఉన్నత పాఠశాల (ZPHS)"

	line = "ఇది ఒక "+phrase+". "

	return line

#Returns TItile from school's name
def getTitle(name):
	phrase =""
	
	if "KGBV" in name:
		phrase = "కస్తూర్బా గాంధీ బాలికా విద్యాలయ (KGBV) "
	elif "MPPS" in name:
		phrase = "మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల (MPPS) "
	elif "MPUPS" in name:
		phrase = "మండల ప్రజా పరిషత్ ప్రాథమికోన్నత పాఠశాల (MPUPS) "
	elif "ZPPS" in name:
		phrase = "జిల్లా పరిషత్ ప్రాథమిక పాఠశాల (ZPPS) "
	elif "ZPHS" in name:
		phrase = "జిల్లా పరిషత్ ఉన్నత పాఠశాల (ZPHS) "

	name = re.sub('^MPPS|^MPUPS|^ZPPS|^ZPHS|^KGBV', '', name)

	title = phrase+transtelugu(name, 1)

	return title

#Returns Grades 
def getGrades(desc):
	p = re.compile(r'[A-Z]+(\d+)-(\d+)')
	m =re.match(p, desc)
	lo =int(m.group(1)); hi =int(m.group(2))

	return lo, hi

#Returns Description about the grades in school
def getClass(lo, hi):
	if lo==1:
		line = "ఇక్కడ విద్యార్థులు "+class_nums[hi] +" తరగతి వరకూ విద్యని అభ్యసించవచ్చు. "
	else:
		line = "ఇందులో "+class_nums[lo]+" తరగతి నుండి "+class_nums[hi]+" తరగతి వరకు విద్యాబోధన కలదు. "
	
	return line

#Returns Infobox
def makeInfobox(details, counts):
	district = transtelugu(details[0].strip(), 0)
	city = transtelugu(details[2].strip(), 0)+", "+district
	students = str(numToTelugu(int(counts[2])+int(counts[3])))
	teachers = str(numToTelugu(int(counts[5])+int(counts[6])))
	lo, hi = getGrades(details[5].strip())
	medium = transtelugu(details[7].strip(), 0)

	title = getTitle(details[4].strip())

	# Make "state" variable
	# Add school type
	infobox = '''\n
{{Infobox school
| name = ''' +title +''' 
| city ='''+city +'''
| district = '''+district +'''
| state = ఆంధ్రప్రదేశ్
| country = భారతదేశము
| grades = '''+str(lo)+'-'+str(hi)+'''
| medium = '''+medium+'''
| students = '''+students +'''
| faculty ='''+teachers +'''
}}\n\n
	'''
	return title, infobox

#Compiles all parts and returns an article for a given school id 
def write(data, df, Id):
	article =""
	# Respective row details from pdf and excel data
	details, counts = getInfo(data, df, Id)
	
	#Sentence for name, village, district and block
	intro = getIntro(details)
	
	#Management
	management =transtelugu(details[6].strip(), 0)
	opts =[management+"నిర్వహణలో ఈ పాఠశాల ఉన్నది. ",
			   "ఇది "+management+"నిర్వహణలో పని చేస్తుంది. "
			 ]

	descLine =getDesc(details)
	oLine =random.choice(opts)
	
	#Classes
	lo, hi = getGrades(details[5].strip())
	cLine = getClass(lo, hi)
	
	#School Medium
	medium = transtelugu(details[7].strip(), 0)
	opts = [medium+"మాధ్యమం లో "+random.choice(["పాఠాలు ", "పాఠములు "])+"బోధిస్తారు. ",
				"ఇక్కడ "+medium+"మాధ్యమం లో "+random.choice(["పాఠాలు ", "పాఠములు "])+"బోధిస్తారు. "
			  ]
	mLine = random.choice(opts)
	
	#School Type & student's counts
	studentStats = getStudentStats(counts)
	
	#Teachers counts + Reference Line
	teacherStats = getTeacherStats(counts)
	
	#Source
	#source ="ఈ వివరములు 2011-12 విద్యా సంవత్సరమునకు సంబంధించినవి. ఇవి నేషనల్ యూనివర్శిటీ ఆఫ్ ఎడ్యుకేషనల్ ప్లానింగ్ అండ్ అడ్మినిస్ట్రేషన్ (NUEPA) జరిపిన సర్వే ఆధారముగా ఇవ్వబడినవి. " 
	source = "ఈ వివరములు నేషనల్ యూనివర్శిటీ ఆఫ్ ఎడ్యుకేషనల్ ప్లానింగ్ అండ్ అడ్మినిస్ట్రేషన్ ([https://www.indiaeducation.net/apexbodies/nuepa/ NUEPA]) జరిపిన సర్వే ఆధారముగా 2011-12 విద్యా సంవత్సరమునకు సంబంధించినవి."

	#Reference
	ref ="&lt;ref&gt;{{cite web |title =School Directory |url =http://udise.in/school_directory.htm |website = udise.in }}&lt;/ref&gt;. "

	# Article Structure
	title, article =makeInfobox(details, counts)

	article =article+descLine+intro+oLine+cLine+mLine
	article =article+"\n\n"+studentStats+teacherStats+ref
	article =article+source

	article =article+"\n\n==మూలాలు==\n {{Reflist}}\n\n[[Category:School]]"
	
	return title, article
	

def main():
	dfile_head = "../DBpckls/"
	pfile_head = "../PDFpckls/"

	dist = "ANANTAPUR"
	data, df, Ids = getData(dfile_head+dist, pfile_head+dist)

	title, article=write(data, df, 28221800503)
	print(article)
	print(title)


if __name__ == "__main__":
	main()