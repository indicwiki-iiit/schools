#coding: utf-8
import re
from transNNP import getTeTokens
from trans import transTelugu, masterHandleTitle
from help import getData, class_nums, numToTelugu

#Returns Grades 
def getGrades(desc):
	p = re.compile(r'[A-Z]+(\d+)-(\d+)')
	m =re.match(p, desc)
	lo =int(m.group(1)); hi =int(m.group(2))

	return lo, hi

# For teluguText.j2
def getData(details, title):
	enName = details[4].strip()
	enMgnt =details[6].strip()
	teMgnt, extraDesc, schToken =getTeTokens(enName, enMgnt)

	village = transTelugu(details[2].strip().lower())
	district = transTelugu(details[0].strip().lower())
	block = transTelugu(details[1].strip().lower())
	code = str(details[3]).strip()

	loInt, hiInt = getGrades(details[5].strip())
	lo =class_nums[loInt]; hi =class_nums[hiInt]
	medium = transTelugu(details[7].strip())

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
		"village": village,
		"district": district,
		"block": block,
		"state":"ఆంధ్రప్రదేశ్",
		"country":"భారతదేశము",
		"code": code,

		"medium": medium,
		"teMgnt": teMgnt,
		"extraDesc": extraDesc,
		"schToken":schToken,
		
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

def getWikiText(details, textTemplate):
	title =masterHandleTitle(details[4].strip())
	data = getData(details, title)
	wikiText = textTemplate.render(data)

	return title, wikiText

if __name__ == '__main__':
	main()
