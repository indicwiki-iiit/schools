import pickle
from flask import request, jsonify
from api import app, pathToData

import gc
from api.utils import getDetails, getOrder

# Routes
@app.route('/get_schoolData', methods=['GET', 'POST'])
def get_schoolData():
	udiseCode=request.json.get('udiseCode')
	try:
		articleParts =pickle.load(open(pathToData+'articleParts.pkl', 'rb'))
		school = articleParts.loc[articleParts['Code']==udiseCode].to_dict('records')[0]

		#Free memory
		del articleParts; gc.collect()

		title = school['Title']
		schoolCats = getDetails(school)
	except:
		print('Failed for udiseCode=', udiseCode, 'of type', type(udiseCode))
		title =''
		schoolCats = []

	return jsonify({ 'title': title, 'schoolCats': schoolCats })

@app.route('/save_schoolCats', methods=['GET', 'POST'])
def save_schoolCats():
	udiseCode=request.json.get('udiseCode')
	newSchoolCats=request.json.get('schoolCats')
	
	articleParts =pickle.load(open(pathToData+'articleParts.pkl', 'rb'))
	for column, value in newSchoolCats:
		articleParts.at[articleParts['Code']==udiseCode, column] =value 

	oldOrder = articleParts.loc[articleParts['Code']==udiseCode, 'Order'].iloc[0]
	newOrder =getOrder(newSchoolCats)
	articleParts.at[articleParts['Code']==udiseCode, 'Order'] =newOrder 
	
	print(oldOrder, newOrder)

	pickle.dump(articleParts, open(pathToData+'articleParts.pkl', 'wb'))

	#Free memory
	del articleParts; gc.collect()

	return jsonify({ 'show': True })
