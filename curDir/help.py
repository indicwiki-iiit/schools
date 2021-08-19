#coding: utf-8
import re
import math
import pickle
import random

##  Global Data: Below  ##

#Data Lists
nums = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100]
teluguN = ['సున్న','ఒకటి','రెండు','మూడు','నాలుగు','అయిదు','ఆరు','ఏడు','ఎనిమిది','తొమ్మిది','పది','పదకొండు','పన్నెండు','పదమూడు','పధ్నాలుగు','పదిహేను','పదహారు','పదిహేడు','పధ్ధెనిమిది','పందొమ్మిది','ఇరవై','ముప్పై','నలభై','యాభై','అరవై','డెబ్బై','ఎనభై','తొంభై','వంద']

#Dictionaries
telugu_nums = {nums[i]:teluguN[i] for i in range(len(nums))}

telugu_letters ={'a': 'ఎ', 'b': 'బి', 'c': 'సి', 'd': 'డి', 'e': 'ఈ', 'f': 'ఎఫ్', 'g': 'జి', 'h': 'హెచ్', 'i': 'అయి', 'j': 'జె', 'k': 'కె', 'l': 'ఎల్', 'm': 'ఎం', 'n': 'ఎన్', 'o': 'ఓ', 'p': 'పి', 'q': 'క్యు', 'r': 'అర్', 's': 'ఎస్', 't': 'టి', 'u': 'యు', 'v': 'వి', 'w': 'డబల్యు', 'x': 'ఎక్స్', 'y': 'వై', 'z': 'జెడ్'}

#Special Lists
sp_nums = ['', 'ఒక','ఇద్దరు','ముగ్గురు','నలుగురు','ఐదుగురు','ఆరుగురు','ఏడుగురు']

class_nums = ['', 'ఒకటవ', 'రెండవ', 'మూడవ', 'నాలుగవ', 'ఐదవ', 'ఆరవ', 'ఏడవ', 'ఎనిమిదవ', 'తొమ్మిదవ', 'పదవ', 'పదకొండవ', 'పన్నెండవ']

# Known Phrases
teluguWord = {"anantapur": "అనంతపూర్", "guntur": "గుంటూర్", "chitoor": "చిత్తూరు", "rural": "రూరల్ ", 
					"telugu": "తెలుగు", "english": "ఇంగ్లీష్", "kannada":"కన్నడ", "colony":"కాలనీ", "school":"పాఠశాల"}

##  Global Data: Above  ##

# dfile -> data from db
# pfile -> data from pdf
def getData(dfile,pfile):
	data = pickle.load(open(dfile,'rb'))
	df = pickle.load(open(pfile,'rb'))
	
	one =data['udise_sch_code'].to_list()
	two =df['Code'].to_list()
	two = [int(t) for t in two]
	
	intersection = sorted(set(one).intersection(set(two)))

	return data, df, intersection

## Helper Funtions: Below ##

#case 0 (end) - pick ONLY from telugu_nums and NO మంది at the end
#case 1 (normal) - pick from telugu_nums and add మంది at the end or sp_nums 
def numToTelugu(Int, case=1):
	if Int < 0:
		return 'nan'
	Int = int(Int)
	
	# Flag to denote if picking from sp_nums
	sp = 0
	
	if Int > 100:
		num =str(Int)
		
	elif 0<Int<8 and case:
		sp =1
		num =sp_nums[Int]
		
	elif Int<=20 or Int in [20,30,40,50,60,70,80,90,100]:
		num =telugu_nums[Int]
	
	else:
		ones =Int%10
		tens = int((Int/10))*10
		num =telugu_nums[tens]+' '+telugu_nums[ones]
		
	if case and not sp:
		num+=' మంది'
		
	return num

def charsToTelugu(abbr,f):
	tChars =''
	
	for c in abbr:
		if c.isalpha():
			c =telugu_letters[c]+f
		tChars+=c
			
	return tChars

def preprocess(phrase):
	new = ''
	for c in phrase:
		if not c.isalpha() and c not in ['.','_']:
			c =' '+c+' '
		new+=c
	
	return new

## Helper Funtions: Above ##