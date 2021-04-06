import pickle
import sweetviz as sv

def makeReport(dataframe, Title):
	report = sv.analyze([dataframe, Title])
	# Default arguments will generate to "SWEETVIZ_REPORT.html"
	report.show_html()
	
def main():
	oneKB =pickle.load(open('data/oneKB.pkl', 'rb'))

	makeReport(oneKB, 'Schools')

if __name__ == '__main__':
	main()