import gc,re, csv, pickle, enchant
from transNNP import handleNewToken, freqTokens
import pandas as pd

# from anuvaad import Anuvaad
# anu =Anuvaad('english-telugu')

from deeptranslit import DeepTranslit
translit = DeepTranslit('telugu').transliterate

threshold = 0.6

# Checks if an attribute value is valid
def is_valid(value):
    if value == None or pd.isnull(value) or str(value) in ["[]", '', "None", 'Not Applicable', 'nan', 'none', 'not applicable']:
        return False
    if isinstance(value, float) or isinstance(value, int):
        return value > 0 and str(value) != 'nan'
    return not value in ['', 'nan', '-1']

def clean(token):
	cleanToken = ''
	for c in token:
		if not re.match(r'[\[\]\(\),]', c):
			cleanToken+=c
	return cleanToken

def masterHandleTitle(title):
	#Pre process
	title = title.upper()
	title = re.sub('&', '&amp;', title)
	title = re.sub(r'(\(\[)', ' \g<1>', title)
	title = re.sub(r'(\)\])', '\g<1> ', title)
	title = re.sub(r'^((MP|ZP|G|GA)(PS|PPS|HS|UPS)|APMS)', '\g<1> ', title)
	title =re.sub('([a-zA-Z])([0-9])', '\g<1> \g<2>', title)
	title =re.sub('([0-9])([a-zA-Z])', '\g<1> \g<2>', title)

	# Translation/Transliteration
	teTitle = ''
	for token in re.split(',+| +', title):
		cleanToken =clean(token)
		withoutDot =re.sub('\.', '', cleanToken)
		# Most Frequent & Imp Tokens
		if cleanToken in freqTokens:
			teToken =freqTokens[cleanToken]
		elif withoutDot in freqTokens:
			teToken =freqTokens[withoutDot]
		# New Token
		else:
			teToken =handleNewToken(cleanToken, translit) 

		try:
			if cleanToken!=token and cleanToken in token:
				teToken = re.sub(cleanToken, teToken, token)
		except:
			teToken =teToken

		teTitle +=teToken+' '

	#Post Processing
	teTitle = re.sub('&', '&amp;', teTitle)
	teTitle = re.sub(r'([\(\[]) ', r'\g<1>', teTitle)
	teTitle = re.sub(r' ([\)\]])', r'\g<1>', teTitle)
	teTitle = re.sub(r'\s+', ' ', teTitle)

	return teTitle.strip()

def process(phrase):
	phr =''

	for word in phrase.split():
		if '_' in word:
			token =''
			parts = word.split('_')
			for p in parts:
				token+=p+' '

			word = token

		word = re.sub('\(', '( ', word)
		word = re.sub('\)', ') ', word)

		phr+=word+' '
			
	return phr.strip()

def handleExceptions(pred, anuTelugu):
	#Take care of అమ్మాయిలు and అబ్బాయిలు
	pred =re.sub('అబ్బాయిలు', 'బాలురు', pred)
	pred =re.sub('అమ్మాయిలు', 'బాలికలు', pred)

	anuTelugu =re.sub('అబ్బాయిలు', 'బాలురు', anuTelugu)
	anuTelugu =re.sub('అమ్మాయిలు', 'బాలికలు', anuTelugu)

	return pred, anuTelugu

def translate(phrase):
	telugu = ''

	for word in phrase.split():
		if '.' in word:
			abbr = ''
			chars = word.split('.')
			for char in chars:
				abbr+=anu.anuvaad(char)+'.'

			telugu+=abbr[:-1]+' '
		else:
			telugu += anu.anuvaad(word)+' '

	return telugu.strip()

def transTelugu(phrase):
	if not is_valid(phrase):
		return 'nan'
	phrase = process(phrase)

	# anuTelugu =translate(phrase)
	anuTelugu = ''
 
	deep =translit(phrase)[0]
	pred =deep['pred']
	prob =float(deep['prob'])

	pred, anuTelugu =handleExceptions(pred, anuTelugu)
	
	if prob >= threshold:
		return pred.strip()+' '
	
	else:
		# return anuTelugu.strip()+' '
		return pred.strip()+' '

def main():
	print(translit('anantapur'))
	# print(anu.anuvaad('anantapur'))
	
if __name__ == "__main__":
	main()
