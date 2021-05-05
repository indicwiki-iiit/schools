import pickle

# Creates a mapping between code to a list of mediums available for that code
def createMap(code_medium):
	cmap ={}
	for code, medium in code_medium:
		if code in cmap:
			cmap[code].append(medium)
		else:
			cmap[code]=[medium]

	return cmap

# Updates the 'Medium' column with the respective value in the codeMap(cmap) created above
def update(halfDB, codeMap):
	# Delete existing duplicates before updating values of 'Medium' column
	halfDB.drop_duplicates(subset='udise_sch_code', keep='first', inplace=True)
	# indices of respective columns
	sch_code =3; sch_medium =7
	# iterate and update according to the codeMap
	for i in range(halfDB.shape[0]):
		try:
			code =halfDB.iat[i, sch_code]
			halfDB.iat[i, sch_medium] =','.join(codeMap[code])
		except:
			print("Failed at", code, codeMap[code])

	return halfDB

def main():
	halfDB = pickle.load(open('halfDB.pkl', 'rb'))
	# Cleans DB, deletes any rows which have 'nan', values
	halfDB.dropna(how='any', inplace=True)

	# List of pair of (code, medium) from the whole DB
	code_medium =halfDB[['udise_sch_code', 'Medium']].values.tolist()
	# Convert that to a map so that key is the code and value is list of medium(s)
	codeMap =createMap(code_medium)

	halfDB = update(halfDB, codeMap)

	print("done ", halfDB.shape)
	pickle.dump(halfDB, open('halfDB.pkl', 'wb'))

if __name__ == '__main__':
	main()