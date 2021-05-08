import re

# Global Variable
cOf ={'Location': 'a', 'Details': 'b', 'Admissions': 'c', 'Academics': 'd', 
		'Faculty': 'e', 'Counts': 'f', 'Achievements': 'g', 'Facilities': 'h', 
		'Extracurricular': 'i', 'History': 'j', 'Ending': 'k', 'References': 'l'}

keyOf ={'a': 'Location', 'b': 'Details', 'c': 'Admissions', 'd': 'Academics',
			'e': 'Faculty', 'f': 'Counts', 'g': 'Achievements', 'h': 'Facilities',
			'i': 'Extracurricular', 'j': 'History', 'k': 'Ending', 'l': 'References'}

# Helper Functions
def getDetails(school):
	# article = ''
	schCats = []
	order =school['Order']
	for c in order:
		key =keyOf[c]
		
		line = school[key].strip()
		if len(line):
			line+=' '
		if key=='References':
			line ='\n \n'+line 

		# article+=line
		schCats.append([key, line])

	return schCats

def getOrder(newCats):
	newOrder = ''
	newCats = [pair[0] for pair in newCats]

	for cat in newCats:
		newOrder+=cOf[cat]

	print("newOrder:", newOrder)
	return newOrder

