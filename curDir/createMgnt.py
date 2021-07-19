import gc, csv, pickle
from trans import masterNNPTrans

def main():
	one = pickle.load(open('./data/oneKB.pkl', 'rb'))

	mgnts =one['SCHMGT_DESC'].unique().tolist()
	mgnts = sorted([m.strip() for m in mgnts])

	for i in range(len(mgnts)):
		mgnts[i] =[mgnts[i], masterNNPTrans(mgnts[i])] 

	print(mgnts)

	csvFile = 'mgnt.csv'
	csvWriter = csv.writer(open(csvFile, 'w'))
	csvWriter.writerow(['English', 'Telugu'])
	csvWriter.writerows(mgnts)
	
	del one
	gc.collect()

if __name__ == '__main__':
	main()