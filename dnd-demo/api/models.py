from api import db

class Schools(db.Model):
	page_id = db.Column(db.Integer, primary_key=True, default=300000)
	udise_id = db.Column(db.Integer, nullable=False, default=300000)

	title =db.Column(db.Text, nullable=False, default='')
	categories =db.Column(db.Text, nullable=False, default="{}")
	
	wordCount = db.Column(db.Integer, nullable=False, default=0)
	
	def __repr__(self):
		return f"School({self.page_id}/{self.udise_id} : '{self.title}' => {self.wordCount})\n"


'''
	default keys of the dictionary saved in "categories"

		['Title', 'Infobox', 'Location', 'Details', 'Academics', 'Counts', 
		'Ending', 'References', 'Facilities', 'Extracurricular', 'Admissions',
		'Faculty', 'History', 'Achievements', 'Order'] and more if added

		keyOf ={'a': 'Location', 'b': 'Details', 'c': 'Admissions', 'd': 'Academics',
					'e': 'Faculty', 'f': 'Counts', 'g': 'Achievements', 'h': 'Facilities',
					'i': 'Extracurricular', 'j': 'History', 'k': 'Ending', 'l': 'References'}
	
	figure out how to add 

'''

def resetDB():
	Schools.query.delete()

def initDB():
	db.create_all()
	db.session.commit()

if __name__ == "__main__":
	initDB()

