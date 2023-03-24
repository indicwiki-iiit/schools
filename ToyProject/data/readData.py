import pickle
import pandas as pd 
import sweetviz as sv

def analyse(df, title):
	report = sv.analyze([df, title])
	report.show_html()

def clean(df):
	for i, row in df.iterrows():
		if str(row.year).startswith('TV'):
			correctyear = 2019
		else:
			correctyear = int(row.year)
		
		df.at[i, 'year'] = correctyear

	return df

def main():
	moviesFile = './movies.csv'
	moviesDF = pd.read_csv(moviesFile)
	moviesDF = clean(moviesDF)
	
	# analyse(moviesDF, 'Movies')

	pickle.dump(moviesDF, open('movies.pkl', 'wb'))

if __name__ == '__main__':
	main()