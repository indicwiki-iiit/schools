# Contains all functions used in template generation
import pandas as pd
import re

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

# Obtains first version of intro line
def get_intro_line_1(village, district, block, cluster, schToken):
    part_1 = ''
    if is_valid(village):
        part_1 = "ఈ " + schToken + village + " గ్రామంలో ఉన్నది. "
    part_2 = ''
    if is_valid(district) and is_valid(block) and is_valid(cluster):
        part_2 = "ఈ గ్రామం " + district + " జిల్లాలో " + block + " పరిధిలో " + cluster + " క్లస్టర్లో ఉన్నది. "
    elif is_valid(district) and is_valid(cluster):
        part_2 = "ఈ గ్రామం " + district + " జిల్లాలో " + cluster + " క్లస్టర్లో ఉన్నది. "
    elif is_valid(district) and is_valid(block):
        part_2 = "ఈ గ్రామం " + district + " జిల్లాలో " + block + " పరిధిలో ఉన్నది. "
    elif is_valid(block) and is_valid(cluster):
        part_2 = "ఈ గ్రామం " + block + " పరిధిలో " + cluster + " క్లస్టర్లో ఉన్నది. "
    elif is_valid(cluster):
        part_2 = "ఈ గ్రామం " + cluster + " క్లస్టర్లో ఉన్నది. "        
    elif is_valid(district):
        part_2 = "ఈ గ్రామం " + district + " జిల్లాలో ఉన్నది. "
    elif is_valid(block):
        part_2 = "ఈ గ్రామం " + block + " పరిధిలో ఉన్నది. "
    return part_1 + part_2

# Obtains second version of intro line
def get_intro_line_2(village, district, block, cluster, schToken):
    part_1 = ''
    if is_valid(village):
        part_1 = "ఈ " + schToken + village + " గ్రామంలో ఉన్నది. "
    part_2 = ''
    if is_valid(district) and is_valid(block) and is_valid(cluster):
        part_2 = district + " జిల్లాలో " + block + " పరిధిలో " + cluster + " క్లస్టర్లో ఈ గ్రామం ఉన్నది. "
    elif is_valid(district) and is_valid(cluster):
        part_2 = district + " జిల్లాలో " + cluster + " క్లస్టర్లో ఈ గ్రామం ఉన్నది. "
    elif is_valid(district) and is_valid(block):
        part_2 = district + " జిల్లాలో " + block + " పరిధిలో ఈ గ్రామం ఉన్నది. "
    elif is_valid(block) and is_valid(cluster):
        part_2 = block + " పరిధిలో " + cluster + " క్లస్టర్లో ఈ గ్రామం ఉన్నది. "
    elif is_valid(cluster):
        part_2 = cluster + " క్లస్టర్లో ఈ గ్రామం ఉన్నది. "     
    elif is_valid(district):
        part_2 = district + " జిల్లాలో ఈ గ్రామం ఉన్నది. "
    elif is_valid(block):
        part_2 = block + " పరిధిలో ఈ గ్రామం ఉన్నది. "
    return part_1 + part_2

# Obtains third version of intro line
def get_intro_line_3(village, district, block, cluster, schToken):
    initial_part = ''
    if is_valid(village):
        initial_part += (village + " గ్రామంలో ")
    if is_valid(district):
        initial_part += (district + " జిల్లాలో ")
    if is_valid(block):
        initial_part += (block + " పరిధిలో ")
    if is_valid(cluster):
        initial_part += (cluster + " క్లస్టర్లో ")
    if len(initial_part) > 0:
        return initial_part +  "ఈ " + schToken + "ఉన్నది. "
    return ''

# Obtains fourth version of intro line
def get_intro_line_4(village, district, block, schToken):
    part_1 = "ఈ " + schToken
    part_2 = ''
    if is_valid(district):
        part_2 = (district + " జిల్లాలో ")
    part_3 = ''
    if is_valid(block):
        part_3 = (block + " పరిధిలో ")
    if is_valid(village):
        if len(part_3) > 0:
            part_3 += "గల "
        elif len(part_2) > 0:
            part_2 += "గల "
    part_4 = ''
    if is_valid(village):
        part_4 = village + " గ్రామంలో "
    if len(part_2) == 0 and len(part_3) == 0 and len(part_4) == 0:
        return ''
    return part_1 + part_2 + part_3 + part_4 + "ఉన్నది. "

# Obtains class info in general
def get_class_info(lo, hi, medium, prefix, suffix):
    if is_valid(lo) and is_valid(hi):
        s2 = ''
        if is_valid(medium):
            s2 = medium + ' మాధ్యమంలో '
        if lo == 0 and hi == 0:
            if is_valid(medium):
                return prefix + s2 + suffix
            return ''
        if lo == hi:
            return prefix + lo + ' తరగతి ' + s2 + suffix
    part_1 = ''
    if is_valid(lo):
        part_1 = lo + ' తరగతి నుండి '
    part_2 = ''
    if(is_valid(hi)):
        part_2 = hi + ' తరగతి వరకు '
    part_3 = ''
    if is_valid(medium):
        part_3 = medium + ' మాధ్యమంలో '
    if len(part_1) == 0 and len(part_2) == 0 and len(part_3) == 0:
        return ''
    return prefix + part_1 + part_2 + part_3 + suffix
    
# Provides info about teachers' count and their genderwise distribution
def get_teacher_info(token, totalTeachers):
    if len(token) == 0:
        if is_valid(totalTeachers):
            return [
                'ఇక్కడ మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులు పని చేస్తున్నారు. ', 
                'ఇక్కడ మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులు ఉన్నారు. '
            ]
        return ['']
    return [
        'ఇక్కడ ' + token + ', మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులు పని చేస్తున్నారు. ',
        'ఇక్కడ మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులు ఉన్నారు. వీరిలో ' + token + '. ',
        'మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులలో ' + token + ' ఇక్కడ పని చేస్తున్నారు. '
    ]
    
# Provides info about students' count and their genderwise distribution
def get_students_info(refLine, token, totalStudents):
    if len(token) == 0:
        if is_valid(totalStudents):
            return [
                refLine + 'ఈ పాఠశాలలో మొత్తం ' + totalStudents + ' విద్యార్థులు విద్యని అభ్యసిస్తున్నారు. ',
            ]
        return ['']
    return [
        refLine + 'ఈ పాఠశాలలో ' + token + ', మొత్తం ' + totalStudents + ' విద్యార్థులు విద్యని అభ్యసిస్తున్నారు. ',
        refLine + 'ఈ పాఠశాలలో మొత్తం ' + totalStudents + ' విద్యార్థులు విద్యని అభ్యసిస్తున్నారు. వీరిలో ' + token + 'ఉన్నారు. ',
        refLine + 'మొత్తం ' + totalStudents + ' విద్యార్థులలో ' + token + 'ఈ పాఠశాల లో విద్యని అభ్యసిస్తున్నారు. '
    ]

# Provides specific details for a given gender - boys / girls
def get_gender_info(refLine, token, gender, suffix):
    if len(token) == 0:
        return ['']
    return [
        refLine + 'ఈ పాఠశాలలో విద్యని అభ్యసిస్తున్న ' + gender + ' సంఖ్య ' + suffix +'. ',
        refLine + 'ఈ పాఠశాలలో ' + token + 'అభ్యసిస్తున్నారు. ',
        refLine + token + 'ఈ పాఠశాలలో అభ్యసిస్తున్నారు. '  
    ]
    
# Describes about school's management and establishment info
def get_management_info(teMgnt, establishment):
    if not is_valid(teMgnt) and not is_valid(establishment):
        return ['']
    sentence_versions = []
    if is_valid(teMgnt) and is_valid(establishment):
        sentence_versions.append(teMgnt + " నిర్వహణలో పని చేస్తున్న ఈ పాఠశాల " + establishment + " లో స్థాపించబడినది.\n")
        sentence_versions.append("ఈ పాఠశాల " + establishment + " లో స్థాపించబడినది, " + teMgnt + " నిర్వహణలో పని చేస్తుంది.\n")
        sentence_versions.append(establishment + " లో స్థాపించబడిన ఈ పాఠశాల " + teMgnt + " నిర్వహణలో పని చేస్తుంది.\n")         
    elif is_valid(establishment):
        sentence_versions.append("ఈ పాఠశాల " + establishment + " లో స్థాపించబడినది.\n")
    return sentence_versions

# Obtain names and links of nearby schools
def get_nearby_schools(nearby_schools):
    required_list = []
    for sch in nearby_schools:
        school, url = tuple(re.split('\s*\#\$\#\s*', sch))
        required_list.append('[' + url + " " + school + ']')
    return ', '.join(required_list)

# Describes board followed by school for grades 10 and 10+2
def get_board_info(board_for_class_10, board_for_class_10_2):
    if not is_valid(board_for_class_10) and not is_valid(board_for_class_10_2):
        return ['']
    if is_valid(board_for_class_10) and is_valid(board_for_class_10_2):
        if board_for_class_10 == board_for_class_10_2:
            return [
                'ఈ పాఠశాల 10 వ తరగతి, 10+2 తరగతులకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది. ',
                'ఈ పాఠశాల 10, 10+2 తరగతుల కొరకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది. '
            ]
        return [
            '10 వ తరగతికి ఈ పాఠశాల ' + board_for_class_10 +' సిలబస్ అనుసరిస్తుంది, 10+2 తరగతులకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది. ',
            'ఈ పాఠశాల 10+2 తరగతులకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది, 10 వ తరగతి కొరకు ' + board_for_class_10 + ' సిలబస్ అనుసరిస్తుంది. ',
            'ఈ పాఠశాల 10 వ తరగతి కొరకు ' + board_for_class_10 + ' సిలబస్, 10+2 తరగతుల  కొరకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది. '
        ]
    elif is_valid(board_for_class_10):
        return [
            '10 వ తరగతికి ఈ పాఠశాల ' + board_for_class_10 +' సిలబస్ అనుసరిస్తుంది. ',
            'ఈ పాఠశాల 10 వ తరగతి కొరకు ' + board_for_class_10 + ' సిలబస్ అనుసరిస్తుంది. '
        ]
    return [
        '10+2 తరగతులకు ఈ పాఠశాల ' + board_for_class_10_2 +' సిలబస్ అనుసరిస్తుంది. ',
        'ఈ పాఠశాల 10+2 తరగతుల కొరకు ' + board_for_class_10_2 + ' సిలబస్ అనుసరిస్తుంది. '      
    ]

# Obtains residential details (like residential type) of school
def get_residential_details(is_residential, residential_type):
    if not is_residential:
        return [
            'ఈ పాఠశాల రెసిడెన్షియల్ పాఠశాల కాదు. ',
            'ఇది రెసిడెన్షియల్ పాఠశాల కాదు. '
        ]
    if not is_valid(residential_type):
        return [
            'ఈ పాఠశాల ఒక రెసిడెన్షియల్ పాఠశాల. ',
            'ఇది ఒక రెసిడెన్షియల్ పాఠశాల. '
        ]
    return [
        'ఈ పాఠశాల ఒక రెసిడెన్షియల్ పాఠశాల, దీని రెసిడెన్షియల్ రకం ' + residential_type + '. ',
        'ఇది ఒక రెసిడెన్షియల్ పాఠశాల. ఈ పాఠశాల రెసిడెన్షియల్ రకం ' + residential_type + '. '
    ]

# Obtains pre primary teachers information
def get_pre_primary_teachers_info(pre_primary_teachers_count):
    if not is_valid(pre_primary_teachers_count) or pre_primary_teachers_count == 0:
        return ['']
    if pre_primary_teachers_count == 1:
        return [
            'వీరిలో ఒక ఉపాధ్యాయుడు ప్రీ ప్రైమరీ తరగతులకు పాఠాలు చెప్తారు. '
        ]
    return [
        'వీరిలో ' + str(pre_primary_teachers_count) + ' ప్రీ ప్రైమరీ తరగతులకు పాఠాలు చెప్తారు. ',
        'వీరిలో ప్రీ ప్రైమరీ తరగతులకు పాఠాలు చెప్పే ఉపాధ్యాయులు ' + str(pre_primary_teachers_count) + '. '
    ]

# Obtains head teacher info (count and names)
def get_head_teachers_info(head_teachers_count, head_teachers_name):
    if (not is_valid(head_teachers_count)) or head_teachers_count == 0:
        return ['']
    if is_valid(head_teachers_name):
        return [
            'ఈ పాఠశాల ప్రధాన ఉపాధ్యాయుడి పేరు ' + head_teachers_name + '. '
        ]
    return [
        'ఈ పాఠశాలకు ఒక ప్రధాన ఉపాధ్యాయుడు ఉన్నారు. '
    ]

# Buildings and class rooms information of a school
def get_building_and_class_rooms_info(building, class_rooms):
    if not is_valid(building) and not is_valid(class_rooms):
        return ['']
    if is_valid(building) and is_valid(class_rooms):
        class_room_string = str(class_rooms) + ' తరగతి గదులు ఉన్నాయి. '
        if class_rooms == 1:
            class_room_string = 'ఒక తరగతి గది ఉంది. '
        return [
            '* ' + 'ఈ పాఠశాల భవనం ఒక ' + building + ' భవనం. ఈ పాఠశాలలో ' + class_room_string + '\n',
            '* ' + 'ఒక ' + building + ' భవనంలో ఈ పాఠశాల స్థాపించబడినది, ఇందులో ' + class_room_string + '\n'
        ]
    elif is_valid(building):
        return [
            '* ' + 'ఈ పాఠశాల భవనం ఒక ' + building + ' భవనం. ' + '\n',
            '* ' + 'ఒక ' + building + ' భవనంలో ఈ పాఠశాల స్థాపించబడినది. ' + '\n'
        ]
    class_room_string = str(class_rooms) + ' తరగతి గదులు ఉన్నాయి. '
    if class_rooms == 1:
        class_room_string = 'ఒక తరగతి గది ఉంది. '
    return [
        '* ' + 'ఈ పాఠశాలలో ' + class_room_string + '\n'
    ]

# Helper function for toilet info
def _t(c):
    if c == 1:
        return ' మరుగుదొడ్డి'
    return ' మరుగుదొడ్లు'
    
#  Information about boys and girls toilets of a school
def get_toilet_info(boys_toilets, girls_toilets):
    if not is_valid(boys_toilets) and not is_valid(girls_toilets):
        return ['']
    if is_valid(boys_toilets) and is_valid(girls_toilets):
        return [
            '* ' + 'ఇక్కడ బాలుర కొరకు ' + str(boys_toilets) + _t(boys_toilets) + ', బాలికల కొరకు ' + str(girls_toilets) + _t(girls_toilets) + ' ఉన్నాయి. ' + '\n',
            '* ' + 'ఇక్కడ ' + str(boys_toilets) + ' బాలుర' + _t(boys_toilets) + ', ' + str(girls_toilets) + ' బాలికల' + _t(girls_toilets) + ' ఉన్నాయి. ' + '\n',
            '* ' + 'ఇక్కడ బాలికల కొరకు ' + str(girls_toilets) + _t(girls_toilets) + ', బాలుర కొరకు ' +  str(boys_toilets) + _t(boys_toilets) + ' ఉన్నాయి. ' + '\n'
        ]
    if is_valid(boys_toilets):
        last_str = ' ఉన్నాయి. '
        if boys_toilets == 1:
            last_str = ' ఉంది. '
        return [
            '* ' + 'ఇక్కడ బాలుర కొరకు ' + str(boys_toilets) + _t(boys_toilets) + last_str + '\n',
            '* ' + 'ఇక్కడ ' + str(boys_toilets) + ' బాలుర' + _t(boys_toilets) + last_str + '\n'
        ]
    last_str = ' ఉన్నాయి. '
    if girls_toilets == 1:
        last_str = ' ఉంది. '
    return [
        '* ' + 'ఇక్కడ బాలికల కొరకు ' + str(girls_toilets) + _t(girls_toilets) + last_str + '\n',
        '* ' + 'ఇక్కడ ' + str(girls_toilets) + ' బాలికల' + _t(girls_toilets) + last_str + '\n'
    ]

# Get information about electricity and drinking water facilities in school
def get_electricity_water_info(electricity, drinking_water):
    if not is_valid(electricity) and not is_valid(drinking_water):
        return ['']
    electricity_str = 'విద్యుత్ ఉంది'
    if not electricity:
        electricity_str = 'విద్యుత్ లేదు'
    water_str = 'త్రాగు నీరు దొరకదు'
    if is_valid(drinking_water):
        if drinking_water != 'బావి':
            water_str = 'త్రాగు నీరు కొరకు ' + drinking_water + ' ఉన్నాయి'
        else:
            water_str = 'త్రాగు నీరు కొరకు ' + drinking_water + ' ఉంది'
    return [
        '* ' + 'ఈ పాఠశాలలో ' + electricity_str + ', ' + water_str + '. ' + '\n',
        '* ' + 'ఈ పాఠశాలలో ' + water_str + ', ' + electricity_str + '. ' + '\n'
    ]

# Get information about kind of wall in school
def get_wall_info(wall):
    if not is_valid(wall):
        return ['']
    poss = ['* ' + 'ఈ పాఠశాల చుట్టూ ' + wall + ' ఉంది. ' + '\n']
    if wall != 'under construction':
        poss.append('* ' + 'ఈ పాఠశాల చుట్టూ ' + wall + ' నిర్మించబడినది. ' + '\n')
    return poss

# Get information about ramps (for disabled people) in school
def get_ramps_info(ramps_for_disabled):
    if not is_valid(ramps_for_disabled) or (not ramps_for_disabled):
        return ['']
    return [
        '* ' + 'ఇక్కడ వికలాంగుల కోసం ర్యాంప్‌లు ఏర్పాటు చేయబడ్డాయి. ' + '\n',
        '* ' + 'ఈ పాఠశాలలో వికలాంగుల కొరకు ర్యాంప్‌లు ఏర్పాటు చేయబడ్డాయి. ' + '\n'
    ]
    
# Get information about library and books count in school
def get_library_and_books_info(library, books_count):
    if not is_valid(library) and not is_valid(books_count):
        return ['']
    library_str = 'ఈ పాఠశాలలో లైబ్రరీ ఉంది. '
    if not library:
        library_str = 'ఈ పాఠశాలలో లైబ్రరీ లేదు. '
        return ['* ' + library_str + '\n']
    if is_valid(books_count) and books_count > 0:
        books_str_1 = 'ఈ లైబ్రరీలో '+ str(books_count) + ' పుస్తకాలు ఉన్నాయి. '
        if books_count == 1:
            books_str_1 = 'ఈ లైబ్రరీలో ఒక పుస్తకం ఉంది. '
        books_str_2 = 'ఈ లైబ్రరీలో ఉన్న పుస్తకాల సంఖ్య ' + str(books_count) + '. '
        return ['* ' + library_str + books_str_1 + '\n', '* ' + library_str + books_str_2 + '\n']
    return ['* ' + library_str + '\n']

# Get information about playground in school
def get_playground_info(playground):
    if not is_valid(playground):
        return ['']
    if playground:
        return [
            '* ' + 'ఈ పాఠశాలలో ఆట స్థలం ఉంది. ' + '\n',
            '* ' + 'ఈ పాఠశాలలో ఆట మైదానం ఉంది. ' + '\n'
        ]
    return [
        '* ' + 'ఈ పాఠశాలలో ఆట స్థలం లేదు. ' + '\n',
        '* ' + 'ఈ పాఠశాలలో ఆట మైదానం లేదు. ' + '\n'
    ]

# Get information about computer aided learning facility and computers in school
def get_computers_info(computer_aided_learning, computers):
    if not is_valid(computer_aided_learning) and not is_valid(computers):
        return ['']
    cal_str = 'కంప్యూటర్ ఎయిడెడ్ లెర్నింగ్ ల్యాబ్ ఉంది. '
    if not computer_aided_learning:
        cal_str = 'కంప్యూటర్ ఎయిడెడ్ లెర్నింగ్ ల్యాబ్ లేదు. '
    if is_valid(computers) and computers > 0:
        comp_str = str(computers) + ' కంప్యూటర్లు ఉన్నాయి'
        if computers == 1:
            comp_str = 'ఒక కంప్యూటర్ ఉంది'
        return [
            '* ' + 'ఈ పాఠశాలలో ' + cal_str + 'ఇక్కడ ' + comp_str + '. ' + '\n',
            '* ' + 'ఈ పాఠశాలలో ' + comp_str + ', ' + cal_str + '\n'
        ]
    return ['* ' + 'ఈ పాఠశాలలో ' + cal_str + '\n']