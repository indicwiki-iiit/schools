import re
import pickle

from anuvaad import Anuvaad
anu =Anuvaad('english-telugu')

from deeptranslit import DeepTranslit
trans = DeepTranslit('telugu').transliterate

# from help import charsToTelugu

threshold = 0.6

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

	return telugu.strip()+' '

def transtelugu(phrase, sch_name):
	phrase = process(phrase)

	anuTelugu =translate(phrase)

	if sch_name:
		return anuTelugu

	deep =trans(phrase)[0]
	pred =deep['pred']
	prob =float(deep['prob'])
	if prob >= threshold:
		return pred+' '
	
	else:
		return anuTelugu

def main():
	# print(trans('anantapur'))
	print(anu.anuvaad('anantapur'))
	
if __name__ == "__main__":
	main()