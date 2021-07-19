import pickle
from jinja2 import Environment, FileSystemLoader

from genXML import tewiki, writePage

from deeptranslit import DeepTranslit 
translit = DeepTranslit('telugu').transliterate

def getData(row):
	global translit
	
	title = translit(row.title.values[0])[0]['pred']
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
		'original_title': row.original_title.values[0],

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
	file_loader = FileSystemLoader('./template/')
	env = Environment(loader=file_loader)
	template = env.get_template('moviesTemplate.j2')

	moviesDF = pickle.load(open('./data/movies.pkl', 'rb'))
	ids = moviesDF.imdb_title_id.tolist()

	fobj = open('movies.xml', 'w')
	fobj.write(tewiki+'\n')

	for i, movieId in enumerate(ids[:3]):
		row = moviesDF.loc[moviesDF['imdb_title_id']==movieId]
		title = row.title.values[0]
		text =template.render(getData(row)) 

		writePage(title, text, fobj)

		print('\n', i, title)

	fobj.write('</mediawiki>')
	fobj.close()

if __name__ == '__main__':
	main()

