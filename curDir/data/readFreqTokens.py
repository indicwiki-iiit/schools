import re, csv, pickle

def clean(token):
	token =token.strip()
	cleanToken = ''
	for c in token:
		if not re.match(r'[\[\]\(\),]', c):
			cleanToken+=c
	return cleanToken

def main():
	# csvObj =csv.reader(open('freqTokens.csv', 'r'))
	csvObj =csv.reader(open('./titles_translation/titleTokens.csv', 'r'))
	pairs = [[row[1],row[2]] for row in csvObj if row[2].strip()!='']
	freqTokens = {}
	for en, te in pairs[1:]:
		cleanToken = clean(en)
		if len(cleanToken)>1:
			cleanTe =clean(te)
			cleanTe = re.sub('&', '&amp;', cleanTe)
			freqTokens[cleanToken]=clean(te)


	# Handle Few School Acronyms separately
	spAcro = {'MPPS':'మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల (MPPS)', 'MPUPS':'మండల ప్రజా పరిషత్ ప్రాథమికోన్నత పాఠశాల (MPUPS)', 'MPPPS':'మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల (MPPS)',
					'KGBV':'కస్తూర్బా గాంధీ బాలికా విద్యాలయ (KGBV)', 'ZPPS':'జిల్లా పరిషత్ ప్రాథమిక పాఠశాల (ZPPS)', 'ZPHS':'జిల్లా పరిషత్ ఉన్నత పాఠశాల (ZPHS)', '(B)':'(బాలుర)', '(G)':'(బాలికల)',
					'GAUPS':'ప్రభుత్వ ఎయిడెడ్  ప్రాథమికోన్నత పాఠశాల (GAUPS)', 'GAPS':'ప్రభుత్వ ఎయిడెడ్  ప్రాథమిక పాఠశాల (GAPS)', 'GAHS':'ప్రభుత్వ ఆశ్రమ ఉన్నత పాఠశాల (GAHS)', 
					'APMS':'ఏపీ మోడల్ స్కూల్ (APMS)', 'APTWRS':'ఆంధ్రప్రదేశ్ గిరిజన సంక్షేమ గురుకుల పాఠశాల', 'GPS':'ప్రభుత్వ ప్రాథమిక పాఠశాల (GPS)',
					'II':'II', 'III':'III', 'WARDI&II':'వార్డ్I&amp;II'
					}
	for sp in spAcro:
		freqTokens[sp] =spAcro[sp]

	pickle.dump(freqTokens, open('./titles_translation/titleTokens.pkl', 'wb'))

if __name__ == '__main__':
	main()