#coding: utf-8
import re
import ast
import pandas as pd
from transNNP import getTeTokens
from trans import transTelugu, masterHandleTitle
from help import getData, class_nums, numToTelugu

# possible values for management
possible_management_values = {
	'Pvt. Aided': 'ప్రైవేట్ ఎయిడెడ్', 'Central Govt.': 'కేంద్ర ప్రభుత్వం', 'Department of Education': 'విద్యా శాఖ', 'Local body': 'స్థానిక సంస్థ',
	'Madarsa Unrecognized': 'మదర్సా (గుర్తించబడలేదు)', 'Tribal/Social Welfare Department': 'గిరిజన/సాంఘిక సంక్షేమ శాఖ', 
 	'Pvt. Unaided': 'ప్రైవేట్ అన్‌ఎయిడెడ్', 'Madarsa Recognized (by Wakf Board/Madarsa Board)': 'మదర్సా (వక్ఫ్ బోర్డు/మదర్సా బోర్డు ద్వారా గుర్తించబడినది)', 
}

# walls possible values dictionary
possible_wall_values = {
	'hedges': 'హెడ్జ్', 'under construction': 'గోడ నిర్మాణంలో', 'pucca': 'పక్కా గోడ', 
 	'partial': 'పాక్షిక గోడ', 'barbed wire fencing': 'ముళ్ల కంచె', 'pucca but broken': 'పక్కా (కానీ విరిగిన) గోడ'
}

# Water possible values dictionary
possible_water_values = {
	'tap water': 'కుళాయిలు', 'well': 'బావి', 'hand pumps': 'హ్యాండ్ పంప్స్'
}

# Buildings possible values dictionary
possible_building_values = {
    'private': 'ప్రైవేట్', 'dilapidated': 'శిథిలావస్థకు చేరిన', 'under construction': 'నిర్మాణంలో ఉన్న', 
    'rent free building': 'అద్దె లేని', 'rented': 'అద్దె', 'government': 'ప్రభుత్వ'
}

# Checks if an attribute value is valid
def is_valid(value):
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, bool):
        return value
    if (value == None) or (pd.isnull(value)) or \
    (str(value) in ["[]", '', "None", 'none', 'N/A', 'n/a', 'Not Applicable', 'not applicable', 'nan', 
                    'Others', 'others', 'No Boundary Wall', 'no boundary wall', 'No Building', 'no building',
                    'Unrecognised', 'unrecognised']):
        return False
    if isinstance(value, float) or isinstance(value, int):
        return value > 0 and str(value) != 'nan'
    return not value in ['', 'nan', '-1']

# Obtains stripped value for attribute
def get_stripped_val(val):
    if not is_valid(val):
        return val
    val2 = val
    if isinstance(val, float):
        val2 = int(val)
    val3 = str(val2)
    return val3.strip(" .-'\n\t")

# Obtains stripped and lower case values for attribute
def get_stripped_lower_val(val):
    if not is_valid(val):
        return val
    val2 = val
    if isinstance(val, float):
        val2 = int(val)
    val3 = str(val2)
    return val3.strip(" .-'\n\t").lower()

#Returns Grades - checks both grade attributes
def getGrades(row):
    desc = get_stripped_val(row['SCHCAT_DESC'])
    if is_valid(desc):
        p = re.compile(r'[A-Z]+(\d+)-(\d+)')
        m =re.match(p, desc)
        lo =int(m.group(1)); hi =int(m.group(2))
        return lo, hi
    class_info = get_stripped_val(row['Classes'])
    if not is_valid(class_info):
        return 0, 0
    spl = class_info.split()
    return int(spl[2]), int(spl[5])

# Returns management info - checks both management attributes
def getManagement(row):
    mgnt = get_stripped_val(row['SCHMGT_DESC'])
    if is_valid(mgnt):
        return mgnt
    return get_stripped_val(row['Management'])

# Translate management if not hard-coded
def getTranslatedManagement(row):
    global possible_management_values
    if not is_valid(row['Management']):
        return row['Management']
    mgnt = get_stripped_val(row['Management'])
    if possible_management_values.get(mgnt) is not None:
        return possible_management_values[mgnt]
    return transTelugu(mgnt)

# converts to int
def get_int(value):
    if not is_valid(value):
        return -1
    return int(value)

# obtains pin code
def get_pin_code(pin):
    if not is_valid(pin):
        return pin
    b = pin.find('(')
    if b == -1:
        return pin
    zip_code = get_stripped_val(pin[:b])
    if len(zip_code) != 6:
        return 'nan'
    return zip_code

# For teluguText.j2
def getData(row, title):
    
    # SCHCAT_DESC -- Classes
	enName = get_stripped_val(row['School Title'])
	enMgnt = getManagement(row)
	teMgnt, extraDesc, schToken =getTeTokens(enName, enMgnt)
	if is_valid(enMgnt) and not is_valid(teMgnt):
		teMgnt = get_stripped_val(row['Management_Telugu'])
		if teMgnt == 'విద్యా శాఖ':
			teMgnt = 'ప్రభుత్వ విద్యా శాఖ'

	village = get_stripped_lower_val(row['Village / Town_Telugu'])
	district = get_stripped_lower_val(row['District_Telugu'])
	block = get_stripped_lower_val(row['Block_Telugu'])
	cluster = get_stripped_lower_val(row['Cluster_Telugu'])
	PIN = get_pin_code(get_stripped_lower_val(row['PIN Code']))
	state = "ఆంధ్రప్రదేశ్"
	if get_stripped_lower_val(row['State'])== 'telangana':
		state = "తెలంగాణ"
	code = get_stripped_val(row['School Code'])

	loInt, hiInt = getGrades(row)
	lo =class_nums[loInt]; hi =class_nums[hiInt]
	medium = get_stripped_val(row['Instruction Medium_Telugu'])
 
	establishment = get_stripped_val(row['Establishment'])
	area = "పట్టణపు"
	if get_stripped_lower_val(row['School Area']) == 'rural':
		area = "గ్రామీణ"
	shifted_to_new_place = get_stripped_lower_val(row['School Shifted to New Place']) == 'yes'
	nearby_schools = ast.literal_eval(get_stripped_val(row['nearby_schools_Telugu']))
 
	is_primary_section_available = get_stripped_lower_val(row['Pre Primary Sectin Avilable']) == 'yes'
	board_for_class_10 = get_stripped_lower_val(row['Board for Class 10th_Telugu'])
	board_for_class_10_2 = get_stripped_lower_val(row['Board for Class 10+2_Telugu'])
	meal = is_valid(row['Meal']) and 'provided' in get_stripped_lower_val(row['Meal'])
	is_residential = get_stripped_lower_val(row['Is School Residential']) == 'yes'
	residential_type = ''
	if get_stripped_lower_val(row['Residential Type']) != 'not applicable':
		residential_type = get_stripped_lower_val(row['Residential Type_Telugu'])
  
	pre_primary_teachers_count = get_int(get_stripped_val(row['Pre Primary Teachers']))
	head_teachers_count = get_int(get_stripped_val(row['Head Teachers']))
	head_teachers_name = get_stripped_lower_val(row['Head Teacher_Telugu'])
 
	building = get_stripped_lower_val(row['Building_Telugu'])
	class_rooms = get_int(get_stripped_lower_val(row['Class Rooms']))
	boys_toilets = get_int(get_stripped_lower_val(row['Boys Toilet']))
	girls_toilets = get_int(get_stripped_lower_val(row['Girls Toilet']))
	electricity = get_stripped_lower_val(row['Electricity']) == 'yes'
	drinking_water = get_stripped_lower_val(row['Drinking Water_Telugu'])
	wall = get_stripped_lower_val(row['Wall_Telugu'])
	if wall == 'పక్కా గోడ':
		wall = 'పక్కా ప్రహరీ గోడ'
	ramps_for_disabled = get_stripped_lower_val(row['Ramps for Disable']) == 'yes'
	library = get_stripped_lower_val(row['Library']) == 'yes'
	books_count = get_int(get_stripped_lower_val(row['Books in Library']))
	playground = get_stripped_lower_val(row['Playground']) == 'yes'
	computer_aided_learning = get_stripped_lower_val(row['Computer Aided Learning']) == 'yes'
	computers = get_int(get_stripped_lower_val(row['Computers']))
   
	sType = get_stripped_lower_val(row['School Type'])
	bInt, gInt = get_int(row['TotalBoysEnrollment']), get_int(row['TotalGirlsEnrollment'])
	bCount =numToTelugu(bInt)
	gCount =numToTelugu(gInt)
	endBCount =numToTelugu(bInt, 0)
	endGCount =numToTelugu(gInt, 0)
	totalStudents =numToTelugu(get_int(row['Total']))

	fInt = get_int(row['Female Teacher'])
	mInt = get_int(row['Male Teachers'])
	fCount =numToTelugu(fInt)
	mCount =numToTelugu(mInt)
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
		"building": building,
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

def get_attribute_and_translation(val):
    if not is_valid(val):
        return ['', '']
    return [val, transTelugu(get_stripped_lower_val(val))]
    
def get_translated_data(row):
    curr_row = [get_stripped_val(row['School Code'])]
    for c in ['School Title', 'Cluster']:
        if not is_valid(row[c]):
            curr_row += ['', '']
            continue
        curr_row += [get_stripped_val(row[c]), masterHandleTitle(get_stripped_val(row[c]))]
    enMngt = getManagement(row)
    if not is_valid(enMngt):
        curr_row += ['', '']
    else:
        curr_row.append(enMngt)
        teMgnt, extraDesc, schToken = getTeTokens(get_stripped_val(row['School Title']), enMngt)
        if is_valid(enMngt) and not is_valid(teMgnt):
            teMgnt = getTranslatedManagement(row)
        curr_row.append(teMgnt)
    building = get_stripped_lower_val(row['Building'])
    if not is_valid(building):
        curr_row += ['', '']
    else:
        curr_row += [building, possible_building_values[building]]
    drinking_water = get_stripped_lower_val(row['Drinking Water'])
    if not is_valid(drinking_water):
        curr_row += ['', '']
    else:
        curr_row += [drinking_water, possible_water_values[drinking_water]]
    wall = get_stripped_lower_val(row['Wall'])
    if not is_valid(wall):
        curr_row += ['', '']
    else:
        curr_row += [wall, possible_wall_values[wall]]
    n_schools, nearby_schools_eng, nearby_schools_tel = ast.literal_eval(get_stripped_val(row['Nearby Schools'])), [], []
    if not is_valid(n_schools):
        curr_row += [[], []]
    else:
        for sch in n_schools:
            school_and_url = re.split('\s*\#\$\#\s*', sch)
            nearby_schools_eng.append(school_and_url[0])
            nearby_schools_tel.append(masterHandleTitle(school_and_url[0]))
        curr_row += [nearby_schools_eng, nearby_schools_tel]
    cols = ['Village / Town', 'District', 'Block', 'Instruction Medium', 'Board for Class 10th', 'Board for Class 10+2', 'Residential Type', 'Head Teacher']   
    for c in cols:
        req_val = get_attribute_and_translation(row[c])
        curr_row += req_val
    return curr_row

def getWikiText(row, textTemplate):
	title = get_stripped_val(row['School Title_Telugu'])
	data = getData(row, title)
	wikiText = textTemplate.render(data)

	return title, wikiText

if __name__ == '__main__':
	main()