import re
import pickle

# from deeptranslit import DeepTranslit
# trans = DeepTranslit('telugu').transliterate

from anuvaad import Anuvaad
anu =Anuvaad('english-telugu')

from help import charsToTelugu

threshold = 0.6

def process(phrase):
	phr =''

	for word in phrase.split():
		if '_' in word:
			parts = word.split('_')
			for p in parts:
				phr+=p+' '
		else:
			phr+=word.lower()+' '
			
	return phr.strip()

def translate(phrase):
	telugu = ''

	for word in phrase.split():
		if len(word)==1:
			telugu +=charsToTelugu(word, '').strip()+' '

		else:
			telugu += anu.anuvaad(word)+' '

	return telugu.strip()+' '

def transtelugu(phrase, sch_name):
	phrase = process(phrase)

	anuTelugu =translate(phrase)

	if sch_name:
		return anuTelugu

	# deep =trans(phrase)[0]
	# pred =deep['pred']
	# prob =float(deep['prob'])
	# if prob >= threshold:
	# 	return pred+' '
	
	# else:
	# 	return anuTelugu
	
	return anuTelugu


def main():
	# print(trans('anantapur'))
	print(anu.anuvaad('anantapur'))
	
if __name__ == "__main__":
	main()