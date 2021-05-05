import pickle

pathToData ='/media/harsha/UDrive/2.IndicWiki/schools/curDir/data'

# Creates a list of dictionary (JS) data
def main():
	articleParts =pickle.load(open(pathToData+'/articleParts.pkl', 'rb'))
	data ="const data =["
	for index, row in articleParts.iterrows():
		row['Title'] =' '.join(row['Title'].split())
		data=data+"\n{'label':'"+row['Title']+"', 'value':'"+str(row['Code'])+"'},"

	data = data[:-1]
	data =data+"\n];\nexport default data;\n"

	print(data)

	fout = open(pathToData+'/schoolNames.js', 'w')
	fout.write(data)
	fout.close()
	print("Move the schoolNames.js to its respective location !")

if __name__ == '__main__':
	main()