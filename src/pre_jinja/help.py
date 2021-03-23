#coding: utf-8
#coding: utf-8

import re
import math
import pickle
import random

from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


##  Global Data: Below  ##

#Data Lists
nums = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100]
teluguN = ['సున్న','ఒకటి','రెండు','మూడు','నాలుగు','అయిదు','ఆరు','ఏడు','ఎనిమిది','తొమ్మిది','పది','పదకొండు','పన్నెండు','పదమూడు','పధ్నాలుగు','పదునయిదు','పదహారు','పదిహేడు','పధ్ధెనిమిది','పందొమ్మిది','ఇరవై','ముప్పై','నలభై','యాభై','అరవై','డెబ్బై','ఎనభై','తొంభై','వంద']

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
teluguL = ['ఎ','బి', 'సి', 'డి', 'ఈ', 'ఎఫ్', 'జి', 'హెచ్', 'అయి', 'జె', 'కె', 'ఎల్', 'ఎం', 'ఎన్', 'ఓ', 'పి', 'క్యు', 'అర్', 'ఎస్', 'టి', 'యు', 'వి', 'డబల్యు', 'ఎక్స్', 'వయి', 'జెడ్']

#Dictionaries
telugu_nums = {nums[i]:teluguN[i] for i in range(len(nums))}

telugu_letters ={letters[i]:teluguL[i] for i in range(len(letters))} 

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
	Int = int(Int)
	
	# Flag to denote if picking from sp_nums
	sp = 0
	
	if Int > 100:
		num =str(Int)
		
	elif 0<Int<8 and case==1:
		sp = 1
		num =sp_nums[Int]
		
	elif Int<=20 or Int in [20,30,40,50,60,70,80,90,100]:
		num =telugu_nums[Int]
	
	else:
		ones =Int%10
		tens = int((Int/10))*10
		num =telugu_nums[tens]+' '+telugu_nums[ones]
		
	if case and not sp:
		num+=' మంది'
		
	return num+' '

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

def toTelugu(phrase):
	tPhrase = ""
	
	phrase = phrase.lower()
	phrase = preprocess(phrase)
	
	words = phrase.split()
	
	spl = ['mpp','zpp','mpps','zphs','mpups','mjpapbcwrs','kgbv','aprei','nclp','icse','govt','cbse','dnt','apswrei','ssa','kgbvs']
	
	dot = '.'
	other = ''
	
	for word in words:
		tPhrase+=' '
		
		if word in teluguWord.keys():
			tPhrase+=teluguWord[word]
		
		elif word in spl or len(word)<3:
			tAbbr = charsToTelugu(word, other)
			tPhrase+=tAbbr
		
		elif '.' in word or '_' in word:
			part =""
			for c in word:
				if c=='.':
					if len(part)==1:
						tPhrase+= charsToTelugu(part,dot)
					else:
						tPhrase+= charsToTelugu(part,other)+'.'
					part =""
				elif c=='_':
					tPhrase+=charsToTelugu(part,other)+'_'
					part =""
				elif c==' ':
					if len(part)<3:
						tPhrase+= charsToTelugu(part,other)
					else:
						tPhrase+=transliterate(part, sanscript.ITRANS, sanscript.TELUGU)+' '
					part = ""
				else:
					part+=c
					
			if part:
				if len(part)<3 or "_" in word:
					tPhrase+= charsToTelugu(part,other)
				else:
					tPhrase+=transliterate(part, sanscript.ITRANS, sanscript.TELUGU)+' '
					
		else:    
			tWord =transliterate(word, sanscript.ITRANS, sanscript.TELUGU) 
			tPhrase+=tWord+' '
	
	#print(phrase, tPhrase.strip())
	#print(tPhrase.strip())
	
	return tPhrase.strip()+' '

## Helper Funtions: Above ##