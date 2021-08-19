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

def get_int(value):
    if value in [None, '', 'nan']:
        return -1
    return int(value)

# For teluguText.j2
def getData(row, title):
	enName = row['School Title'].strip()
	enMgnt =row['SCHMGT_DESC'].strip()
	teMgnt, extraDesc, schToken =getTeTokens(enName, enMgnt)

	village = transTelugu(row['Village / Town'].strip().lower())
	district = transTelugu(row['District'].strip().lower())
	block = transTelugu(row['Block'].strip().lower())
	code = row['School Code'].strip()

	loInt, hiInt = getGrades(row['SCHCAT_DESC'].strip())
	lo =class_nums[loInt]; hi =class_nums[hiInt]
	medium = transTelugu(row['Instruction Medium'].strip())

	sType =row['School Type'].lower()
	bInt, gInt = get_int(row['TotalBoysEnrollment']), get_int(row['TotalGirlsEnrollment'])
	bCount =numToTelugu(row['TotalBoysEnrollment'])
	gCount =numToTelugu(row['TotalGirlsEnrollment'])
	endBCount =numToTelugu(row['TotalBoysEnrollment'], 0)
	endGCount =numToTelugu(row['TotalGirlsEnrollment'], 0)
	totalStudents =numToTelugu(row['Total'])

	fInt = get_int(row['Female Teacher'])
	mInt = get_int(row['Male Teachers'])
	fCount =numToTelugu(row['Female Teacher'])
	mCount =numToTelugu(row['Male Teachers'])
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

def getWikiText(row, textTemplate):
	title =masterHandleTitle(row['School Title'].strip())
	data = getData(row, title)
	wikiText = textTemplate.render(data)

	return title, wikiText

if __name__ == '__main__':
	main()
