import re, csv, pickle
from collections import defaultdict

def main():
	# data
	one =pickle.load(open('./oneKB.pkl', 'rb'))
	names = one['School Name'].tolist()

	# Count tokens
	countOf = defaultdict(lambda: 0)
	allNames = ' '.join(names)
	allNames =re.sub(r'\(', ' (', allNames)
	allNames =re.sub(r'\)', ') ', allNames)
	for token in allNames.split():
		if re.match(r'.*[a-zA-Z].*', token):
			countOf[token]+=1

	# Print Values
	keys = list(countOf.keys())
	pairs = sorted([(countOf[key], key) for key in keys], reverse=True)

	csvWriter = csv.writer(open('tokens.csv', 'w'))
	csvWriter.writerow(['Count', 'Eng Token', 'Telugu'])
	for pair in pairs:
		csvWriter.writerow([pair[0], pair[1]])

	print('Total:', len(pairs))

if __name__ == '__main__':
	main()

