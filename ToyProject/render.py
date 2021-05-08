import pickle
from jinja2 import Environment, FileSystemLoader

# from anuvaad import Anuvaad
# telugu = Anuvaad('english-telugu')
# from deeptranslit import DeepTranslit
# trans = DeepTranslit('telugu').transliterate

from genXML import tewiki, writePage

def getData(row):
	# Translation and Transliteration
	try:
		title = row.title.values[0]
		anu_title = telugu.anuvaad(row.title.values[0])
		deep = trans(title)[0]
		if float(deep['prob']) >= 0.070:
			title = deep['pred']
		else:
			title = anu_title		
	except:
		title =row.title.values[0]

	# Data dictionary 
	data = {
		#{%- macro info(title, id, year, genre, actors, duration, country, original_title) -%}
		'title':title,
		'id': row.imdb_title_id.values[0], 
		'year': row['year'].values[0], 
		'genre': row.genre.values[0],
		'actors': row.actors.values[0],
		'duration': row.duration.values[0],
		'country': row.country.values[0],

		#{%- macro crew(director, language, writer, production_company) -%}
		'director':row.director.values[0],
		'language':row.language.values[0],
		'writer':row.writer.values[0],
		'production_company':row.production_company.values[0],

		#{%- macro numbers(avg_vote, budget) -%}
		'avg_vote':row.avg_vote.values[0],
		'budget':row.budget.values[0]
	}

	return data

def main():
	file_loader = FileSystemLoader('./template')
	env = Environment(loader=file_loader)
	template = env.get_template('moviesTemplate.j2')

	moviesDF =pickle.load(open('./data/moviesDF.pkl', 'rb'))

	ids = moviesDF.imdb_title_id.tolist()
	ids =ids[:3] #remove this to generate articles for all movies

	# Initiate the file object
	fobj = open('movies.xml', 'w')
	fobj.write(tewiki+'\n')

	for i, movieId in enumerate(ids):
		row = moviesDF.loc[moviesDF['imdb_title_id']==movieId]
		title = row.title.values[0]
		text = template.render(getData(row))

		writePage(title, text, fobj)		

		print(i, title)
		print(text, '\n')

	fobj.write('</mediawiki>')
	fobj.close()

if __name__ == '__main__':
	main()