import pickle
import pandas as pd

def clean(moviesDF):
	for i, row in moviesDF.iterrows():
		if str(row.year).startswith('TV'):
			print(row.year)
			correctYear = 2019
		else:
			correctYear = int(row.year)

		moviesDF.at[i, 'year'] = correctYear

	moviesDF = moviesDF.dropna()

	return moviesDF

def main():
	moviesFile = './movies.csv'
	moviesDF = pd.read_csv(moviesFile)
	moviesDF = clean(moviesDF)

	pickle.dump(moviesDF, open('./moviesDF.pkl', 'wb'))


if __name__ == '__main__':
	main()