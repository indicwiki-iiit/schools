#coding: utf-8
import re
import ast
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
	cluster = transTelugu(row['Cluster'].strip().lower())
	PIN = transTelugu(row['PIN Code'].strip().lower())
	state = "ఆంధ్రప్రదేశ్"
	if row['State'].strip().lower() == 'telangana':
		state = "తెలంగాణ"
	code = row['School Code'].strip()

	loInt, hiInt = getGrades(row['SCHCAT_DESC'].strip())
	lo =class_nums[loInt]; hi =class_nums[hiInt]
	medium = transTelugu(row['Instruction Medium'].strip())
 
	establishment = row['Establishment'].strip()
	area = "పట్టణపు"
	if row['School Area'].strip().lower() == 'rural':
		area = "గ్రామీణ"
	shifted_to_new_place = row['School Shifted to New Place'].strip().lower() == 'yes'
	n_schools, nearby_schools = ast.literal_eval(row['Nearby Schools'].strip()), []
	for sch in n_schools:
		school_and_url = re.split('\s*#$#\s*', sch)
		school_name = transTelugu(school_and_url[0])
		nearby_schools.append(school_name + ' #$# ' + school_and_url[1])
 
	is_primary_section_available = row['Pre Primary Sectin Avilable'].strip().lower() == 'yes'
	board_for_class_10 = transTelugu(row['Board for Class 10th'].strip.lower())
	board_for_class_10_2 = transTelugu(row['Board for Class 10+2'].strip.lower())
	meal = 'provided' in row['Meal'].strip.lower()
	is_residential = row['Is School Residential'].strip().lower() == 'yes'
	residential_type = ''
	if row['Residential Type'].strip().lower() != 'not applicable':
		residential_type = transTelugu(row['Residential Type'].strip().lower())
  
	pre_primary_teachers_count = get_int(row['Pre Primary Teachers'].strip())
	head_teachers_count = get_int(row['Head Teachers'].strip())
	head_teachers_name = transTelugu(row['Head Teacher'].strip().lower())
 
	buidling = transTelugu(row['Building'].strip().lower())
	class_rooms = get_int(row['Class Rooms'].strip())
	boys_toilets = get_int(row['Boys Toilet'].strip())
	girls_toilets = get_int(row['Girls Toilet'].strip())
	electricity = row['Electricity'].strip().lower() == 'yes'
	drinking_water = transTelugu(row['Drinking Water'].strip().lower())
	wall = transTelugu(row['Wall'].strip().lower())
	ramps_for_disabled = row['Ramps for Disable'].strip().lower() == 'yes'
	library = row['Library'].strip().lower() == 'yes'
	books_count = get_int(row['Books in Library'].strip())
	playground = row['Playground'].strip().lower() == 'yes'
	computer_aided_learning = row['Computer Aided Learning'].strip().lower() == 'yes'
	computers = get_int(row['Computers'].strip())
   
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
		# intro(village, district, block, cluster, PIN, schToken, teMgnt)
		"title": title,
		"village": village,
		"district": district,
		"block": block,
		"state": state,
		"cluster": cluster,
		"PIN": PIN,
		"schToken":schToken,
		"country":"భారతదేశము",

  		# classes(lo, hi, medium, extraDesc)
		"lo": lo, #the transliteration of lower class in telugu
		"hi": hi, #the transliteration of higher class in telugu
		"medium": medium,
		"extraDesc": extraDesc,

		# codeAndLocality(code, teMgnt, establishment, area, shifted_to_new_place, nearby_schools)
		"code": code,
		"teMgnt": teMgnt,
		"establishment": establishment,
		"area": area,
		"shifted_to_new_place": shifted_to_new_place,
		"nearby_schools": nearby_schools,
    
		# academicInfo(is_primary_section_available, board_for_class_10, board_for_class_10_2, meal, is_residential, residential_type)
		"is_primary_section_available": is_primary_section_available,		
		"board_for_class_10": board_for_class_10,
		"board_for_class_10_2": board_for_class_10_2,
		"meal": meal,
		"is_residential": is_residential,
		"residential_type": residential_type,
		
		# studentsCount(sType, bInt, gInt, bCount, gCount, totalStudents, endBCount, endGCount)
		'sType': sType,
		'bInt': bInt, 
  		'gInt': gInt,
		'bCount': bCount, 'endBCount': endBCount,
		'gCount': gCount, 'endGCount': endGCount,
		'totalStudents': totalStudents,

		# teachersCount(mInt, mCount, fInt, fCount, totalTeachers)
		'mInt': mInt,
		'mCount': mCount,
		'fInt': fInt,
		'fCount': fCount,
		'totalTeachers': totalTeachers, 
  
		# teacherPositions(pre_primary_teachers_count, head_teachers_count, head_teachers_name)
		"pre_primary_teachers_count": pre_primary_teachers_count,
		"head_teachers_count": head_teachers_count,
		"head_teachers_name": head_teachers_name,
  
		# infrastructure(building, class_rooms, boys_toilets, girls_toilets, electricity, drinking_water, wall, ramps_for_disabled, library, books_count, playground, computer_aided_learning, computers)
		"building": buidling,
		"class_rooms": class_rooms,
		"boys_toilets": boys_toilets,
		"girls_toilets": girls_toilets,
		"electricity": electricity,
		"drinking_water": drinking_water,
		"wall": wall,
		"ramps_for_disabled": ramps_for_disabled,
		"library": library,
		"books_count": books_count,
		"playground": playground,
		"computer_aided_learning": computer_aided_learning,
		"computers": computers,
  
		# infobox(title, village, district, state, country, loInt, hiInt, medium, totalStudents, PIN, establishment)
		"loInt": loInt,
		"hiInt": hiInt
	}

	return data

def getWikiText(row, textTemplate):
	title =masterHandleTitle(row['School Title'].strip())
	data = getData(row, title)
	wikiText = textTemplate.render(data)

	return title, wikiText

if __name__ == '__main__':
	main()
