# Just a helper file for trans
import re, pickle, enchant

# GLOBAL
threshold = 0.6
en = enchant.Dict('en_us')

stopWords = {'of', 'on', 'at', 'an', 'it'}
teluguChar ={'a': 'ఎ', 'b': 'బి', 'c': 'సి', 'd': 'డి', 'e': 'ఈ', 'f': 'ఎఫ్', 'g': 'జి', 'h': 'హెచ్', 'i': 'అయి', 'j': 'జె', 'k': 'కె', 'l': 'ఎల్', 'm': 'ఎం', 'n': 'ఎన్', 'o': 'ఓ', 'p': 'పి', 'q': 'క్యు', 'r': 'అర్', 's': 'ఎస్', 't': 'టి', 'u': 'యు', 'v': 'వి', 'w': 'డబల్యు', 'x': 'ఎక్స్', 'y': 'వై', 'z': 'జెడ్'}

Mgnts ={'AP MODEL SCHOOLS':'ఎ.పి మోడల్ పాఠశాలలు', 'AP Sports School run by govt':'ప్రభుత్వ ఎ.పి స్పోర్ట్స్  పాఠశాల', 'APREI Society Schools':' ఆంధ్రప్రదేశ్ రెసిడెన్షియల్ ఎడ్యుకేషనల్ ఇనిస్టిట్యూషన్స్ సొసైటీ పాఠశాలలు', 'APSWREI Society Schools':'ఆంధ్రప్రదేశ్ సాంఘిక సంక్షేమ గురుకుల సొసైటీ పాఠశాలలు', 'APTWREI Society Schools':'ఆంధ్రప్రదేశ్ గిరిజన సంక్షేమ గురుకుల పాఠశాలలు',
			'Boarstal or Juvenille Schools':'బోర్స్టల్ లేక బాల నేరస్తుల పాఠశాల', 'GOVT TW DEPT.PRIMARY SCHOOLS':'ప్రభుత్వ గిరిజన సంక్షేమ శాఖ ప్రాథమిక పాఠశాల', 'Govt. Oriental Schools':'ప్రభుత్వ ప్రాచ్య పాఠశాలలు', 'Govt.Schools':'ఫ్రభుత్వ పాఠశాలలు', 'KGBVs(SSA)':'కస్తూర్భా గాంధీ బాలిక విద్యాలయ (సర్వ శిక్ష అభియాన్)',
			'Kendriya Vidyalaya':'కేంద్రియా విద్యాలయ', 'MPP_ZPP SCHOOLS':'మండల ప్రజా పరిషత్తు_జిల్లా ప్రజా పరిషత్తు పాఠశాలలు', 'MUNCIPAL':'మున్సిపల్', 'NCLP':'జాతీయ బాల కార్మిక ప్రాజెక్ట్', 'Navodaya Vidyalaya':'నవోదయ విద్యాలయ', 'Pvt.Aided':'ప్రైవేట్ ఎయిడెడ్', 'Pvt.Aided Oriental Schools':'ప్రైవేట్ ఎయిడెడ్ ప్రాచ్య పాఠశాలలు', 'Pvt.Aided Sanskrit patashalas':'ప్రైవేట్ ఎయిడెడ్ సంసృత పాఠశాలలు', 
			'Pvt.Unaided':'ప్రైవేట్ అన్‌ఎయిడెడ్', 'Pvt.Unaided Oriental Schools':'ప్రైవేట్ అన్‌ఎయిడెడ్ ప్రాచ్య పాఠశాల', 'State Govt.':'రాష్ట్ర ఫ్రభుత్వ', 'State Govt.(DNT)':'రాష్ట్ర ఫ్రభుత్వ (డి.ఎన్.టి.)', 'TW DEPT. ASHRAM SCHOOLS':'గిరిజన సంక్షేమ ఆశ్రమ పాఠశాలలు'
			}

spAcro = {'MPPS':'మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల ', 'MPUPS':'మండల ప్రజా పరిషత్ ప్రాథమికోన్నత పాఠశాల ', 'MPPPS':'మండల ప్రజా పరిషత్ ప్రాథమిక పాఠశాల ',
				'KGBV':'కస్తూర్బా గాంధీ బాలికా విద్యాలయ ', 'ZPPS':'జిల్లా పరిషత్ ప్రాథమిక పాఠశాల ', 'ZPHS':'జిల్లా పరిషత్ ఉన్నత పాఠశాల ', 
				'GAUPS':'ప్రభుత్వం ఎయిడెడ్  ప్రాథమికోన్నత పాఠశాల ', 'GAPS':'ప్రభుత్వం ఎయిడెడ్  ప్రాథమిక పాఠశాల ', 'GAHS':'ప్రభుత్వ ఆశ్రమ ఉన్నత పాఠశాల ', 
				'APMS':'ఏపీ మోడల్ స్కూల్ ', 'APTWRS':'ఆంధ్రప్రదేశ్ గిరిజన సంక్షేమ గురుకుల పాఠశాల ', 'GPS':'ప్రభుత్వ ప్రాథమిక పాఠశాల '
			}

extraDescOf ={'Blind':'ఇది అంధుల పాఠశాల. ', 'Deaf and Dumb':'ఇది చెవిటి మరియు మూగవారి వల పాఠశాల. ', 'Mentally Retarded':'ఇది బుద్ధిమాంద్యుల పాఠశాల. ', 'CBSE':'ఈ పాఠశాల సి.బి.ఎస్.ఈ. సిలబస్ అనుసరిస్తుంది. ', 'ICSE':'ఈ పాఠశాల అయి.సి.ఎస్.ఈ. సిలబస్ అనుసరిస్తుంది. '}

# freqTokens = pickle.load(open('./data/freqTokens.pkl', 'rb'))
freqTokens = pickle.load(open('./data/titles_translation/titleTokens.pkl', 'rb'))

# Functions

# def clean():
#   names = re.sub('\(N[O0]([.-])', '\(NUMBER\g<1>', names)
#   possible = [word for word in names.split() if sum(c.isalpha() for c in word)<5]
#   possible = set(possible)

def transAcronym(token):
	global teluguChar
	telugu = ''
	for c in token:
		if c.isalpha():
			c =teluguChar[c]+'.'

		telugu+=c
	return telugu

def noVowelin(token):
	token = token.lower()
	for c in 'aeiou':
		if c in token:
			return False
	return True

# This funtion is called from write.py's getTitleData function
def handleNewToken(token, translit):
	global en, stopWords, threshold
	token = token.lower()
	
	teToken = ''

	#Case1: Handle Number separately
	if re.match(r'(\(?)n[o0]([.-]?\d)(\)?)', token):
		teToken = re.sub(r'(\(?)n[o0]([.-]?\d)(\)?)', r'\g<1>నెం\g<2>\g<3>', token)
		if not re.match('[a-zA-Z]', teToken):
			return teToken

	#Case2: Tokens split by any char other than alphabet and numbers
	for subToken in re.split(r'[^a-zA-Z0-9]+', token):
		slen =len(subToken)
		if subToken.upper() in freqTokens:
			teToken+=' '+freqTokens[subToken.upper()]+' '
		elif slen==1:
			if subToken.isalpha():
				teToken+=teluguChar[subToken]+'.'
			else:
				teToken+=subToken+' '
		elif re.match(r'^(sis|apiic|dept)$', subToken) or (slen<3 and not subToken in stopWords) or (slen==3 and not en.check(subToken)) or noVowelin(subToken):
			teToken+=' '+transAcronym(subToken)
		else:
			subToken = subToken.upper()
			deep_telugu = translit(subToken)[0]
			teToken+=' '+deep_telugu['pred']
	
	# Translation Exceptions
	teToken =re.sub('స్కూల్', 'పాఠశాల',teToken)
	teToken =re.sub('బాయ్స్','బాలురు', teToken)
	teToken =re.sub('గిర్ల్స్','బాలికలు', teToken)

	return teToken

#Function to handle school's management mainly and send other tokens
#	used in write.py (getData())
def getTeTokens(enName, enMgnt):
	#teMgnt
	teMgnt = ''
	try:
		if enMgnt in Mgnts:
			teMgnt =Mgnts[enMgnt]
		if teMgnt =='':
			if 'Govt.Schools' in enMgnt:
				teMgnt ='ఫ్రభుత్వ పాఠశాలలు'
			elif 'Pvt.Unaided' in enMgnt:
				teMgnt ='ప్రైవేట్ అన్‌ఎయిడెడ్'
	except:
		pass

	# extraDesc
	extraDesc =''
	try:
		for key in extraDescOf:
			if key in enMgnt:
				extraDesc =extraDescOf[key]
	except:
		pass

	#schToken
	schToken = 'పాఠశాల '
	try:
		if enName.split()[0] in spAcro:
			schToken = spAcro[enName.split()[0]]
		elif 'Govt.Schools' in enMgnt: 
			schToken ='ఫ్రభుత్వ పాఠశాల '
		elif 'Pvt.Unaided' in enMgnt:
			schToken ='ప్రైవేట్ పాఠశాల '
		elif 'Pvt.Aided' in enMgnt:
			schToken ='ప్రైవేట్ ఎయిడెడ్ పాఠశాల '
	except:
		pass
   

	return teMgnt, extraDesc, schToken
