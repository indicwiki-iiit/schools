#coding: utf-8

import re
from trans import transtelugu
from help import getData, class_nums, numToTelugu

from jinja2 import Environment, FileSystemLoader

# For teluguTitle.j2
def getSchName(name):
	data ={}
	data['enName']=name

	name = re.sub('^MPPS|^MPUPS|^ZPPS|^ZPHS|^KGBV', '', name)
	teName =transtelugu(name, 1)
	data['teName']= teName

	return data

#Returns Grades 
def getGrades(desc):
	p = re.compile(r'[A-Z]+(\d+)-(\d+)')
	m =re.match(p, desc)
	lo =int(m.group(1)); hi =int(m.group(2))

	return lo, hi

# For teluguText.j2
def getData(details, title):
	names = getSchName(details[4].strip())
	enMgnt =details[6].strip()
	teMgnt =transtelugu(details[6].strip(), 0)

	village = transtelugu(details[2].strip(), 0)
	district = transtelugu(details[0].strip(), 0)
	block = transtelugu(details[1].strip(), 0)
	code = str(details[3]).strip()

	loInt, hiInt = getGrades(details[5].strip())
	lo =class_nums[loInt]; hi =class_nums[hiInt]
	medium = transtelugu(details[7].strip(), 0)

	sType =details[9].lower()
	bInt, gInt =details[11], details[12]
	bCount =numToTelugu(details[11])
	gCount =numToTelugu(details[12])
	endBCount =numToTelugu(details[11], 0)
	endGCount =numToTelugu(details[12], 0)
	totalStudents =numToTelugu(details[13])

	fInt =int(details[15])
	mInt =int(details[14])
	fCount =numToTelugu(details[15])
	mCount =numToTelugu(details[14])
	totalTeachers =numToTelugu(fInt+mInt)

	data = {
		"title": title,
		"enName": names['enName'],
		"village": village,
		"district": district,
		"block": block,
		"state":"ఆంధ్రప్రదేశ్",
		"country":"భారతదేశము",
		"code": code,

		"medium": medium,
		"enMgnt": enMgnt,
		"teMgnt": teMgnt,

		"lo": lo, #the transliteration of lower class in telugu
		"loInt": loInt,
		"hi": hi, ##the transliteration of higher class in telugu
		"hiInt": hiInt,
		
		'sType': sType,
		'totalStudents': totalStudents,
		'bInt': bInt, 'gInt': gInt,
		'bCount': bCount, 'endBCount': endBCount,
		'gCount': gCount, 'endGCount': endGCount,

		'mInt': mInt,
		'mCount': mCount,
		'fInt': fInt,
		'fCount': fCount,
		'totalTeachers': totalTeachers
	}

	return data



def getWikiText(details, titleTemplate, textTemplate):
	title =titleTemplate.render(getSchName(details[4].strip()))
	# print("Title:", details[4].strip(), title)
	data = getData(details, title)
	wikiText = textTemplate.render(data)
	print(wikiText, "\n")

	return title, wikiText


if __name__ == '__main__':
	main()
