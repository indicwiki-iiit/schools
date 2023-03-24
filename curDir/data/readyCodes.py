# This script selects school udise codes which do not have duplicate school names.
# Selects codes for which articles can be generated
import pickle

def main():
	#Data
	oneKB = pickle.load(open('oneKB.pkl', 'rb'))

	names = oneKB['School Name'].tolist()

	nameCodes =oneKB[['School Name', 'School Code']].values.tolist()
	codeOf = {}
	for nc in nameCodes:
		codeOf[nc[0]] = nc[1]

	# All School Codes
	allCodes = oneKB['School Code'].tolist()
	print('All:', len(allCodes))
	# Calculate codes of duplicate names
	dupCodes = [nc[1] for nc in nameCodes if names.count(nc[0])>1]
	print('Dups:', len(dupCodes))
	# Other codes which are ready !
	codes = [code for code in allCodes if code not in dupCodes]
	print('Ready:', len(codes))

	pickle.dump(codes, open('readyCodes.pkl', 'wb'))

if __name__ == '__main__':
	main()