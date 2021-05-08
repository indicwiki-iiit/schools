import pickle, json
from api import db, pickleFolder
from api.models import Schools

def	populateSchools():
	print('Deleted '+str(Schools.query.delete())+' school(s) !')
	part100 = pickle.load(open(pickleFolder+'parts100.pkl', 'rb')) #this is a dataframe
	cnt = 0
	for _,row in part100.iterrows():
		categories = [('Location',row['Location']), ('Details', row['Details']), ('Admissions', row['Admissions']), ('Academics', row['Academics']),
						('Faculty', row['Faculty']), ('Counts', row['Counts']), ('Achievements', row['Achievements']), ('Facilities', row['Facilities']),
						('Extracurricular', row['Extracurricular']), ('History', row['History']), ('Ending', row['Ending']), ('References', row['References'])
					]
		wc = len(' '.join([text for _, text in categories]))
		title = ' '.join(row['Title'].strip().split())
		obj = Schools(page_id=row['PageID'], udise_id=row['Code'], title=title, 
							categories=json.dumps(categories), wordCount=wc)

		db.session.add(obj)
		cnt+=1
	
	print('Added '+str(cnt)+' school(s)!')

	db.session.commit()

if __name__=="__main__":
	populateSchools()
