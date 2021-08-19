# Contains all functions used in template generation
import pandas as pd

# Checks if an attribute value is valid
def is_valid(value):
    if value == None or pd.isnull(value) or str(value) in ["[]", '', "None", 'Not Applicable', 'nan']:
        return False
    if isinstance(value, float) or isinstance(value, int):
        return value > 0 and str(value) != 'nan'
    return not value in ['', 'nan', '-1']

# Obtains first version of intro line
def get_intro_line_1(village, district, block, schToken):
    part_1 = ''
    if is_valid(village):
        part_1 = "ఈ " + schToken + village + "గ్రామంలో ఉన్నది. "
    part_2 = ''
    if is_valid(district) and is_valid(block):
        part_2 = "ఈ గ్రామం " + district + "జిల్లాలో " + block + "పరిధిలో ఉన్నది. "
    elif is_valid(district):
        part_2 = "ఈ గ్రామం " + district + "జిల్లాలో ఉన్నది. "
    elif is_valid(block):
        part_2 = "ఈ గ్రామం " + block + "పరిధిలో ఉన్నది. "
    return part_1 + part_2

# Obtains second version of intro line
def get_intro_line_2(village, district, block, schToken):
    part_1 = ''
    if is_valid(village):
        part_1 = "ఈ " + schToken + village + "గ్రామంలో ఉన్నది. "
    part_2 = ''
    if is_valid(district) and is_valid(block):
        part_2 = district + "జిల్లాలో " + block + "పరిధిలో ఈ గ్రామం ఉన్నది. "
    elif is_valid(district):
        part_2 = district + "జిల్లాలో ఈ గ్రామం ఉన్నది. "
    elif is_valid(block):
        part_2 = block + "పరిధిలో ఈ గ్రామం ఉన్నది. "
    return part_1 + part_2

# Obtains third version of intro line
def get_intro_line_3(village, district, block, schToken):
    initial_part = ''
    if is_valid(district):
        initial_part += (district + "జిల్లాలో ")
    if is_valid(block):
        initial_part += (block + "పరిధిలో ")
    if is_valid(village):
        initial_part += (village + "గ్రామంలో ")
    if len(initial_part) > 0:
        return initial_part +  "ఈ " + schToken + "ఉన్నది. "
    return ''

# Obtains fourth version of intro line
def get_intro_line_4(village, district, block, schToken):
    part_1 = "ఈ " + schToken
    part_2 = ''
    if is_valid(district):
        part_2 = (district + "జిల్లాలో ")
    part_3 = ''
    if is_valid(block):
        part_3 = (block + "పరిధిలో ")
    if is_valid(village):
        if len(part_3) > 0:
            part_3 += "గల "
        elif len(part_2) > 0:
            part_2 += "గల "
    part_4 = ''
    if is_valid(village):
        part_4 = village + "గ్రామంలో "
    if len(part_2) == 0 and len(part_3) == 0 and len(part_4) == 0:
        return ''
    return part_1 + part_2 + part_3 + part_4 + "ఉన్నది. "

# Obtains class info in general
def get_class_info(lo, hi, medium, prefix, suffix):
    part_1 = ''
    if is_valid(lo):
        part_1 = lo + ' తరగతి నుండి '
    part_2 = ''
    if(is_valid(hi)):
        part_2 = hi + ' తరగతి వరకు '
    part_3 = ''
    if is_valid(medium):
        part_3 = medium + 'మాధ్యమంలో '
    if len(part_1) == 0 and len(part_2) == 0 and len(part_3) == 0:
        return ''
    return prefix + part_1 + part_2 + part_3 + suffix
    
# Provides info about teachers' count and their genderwise distribution
def get_teacher_info(token, totalTeachers):
    if len(token) == 0:
        if is_valid(totalTeachers):
            return [
                'ఇక్కడ  మొత్తం ' + totalTeachers + ' ఉపాధ్యాయులు పని చేస్తున్నారు. ', 
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
    