import React, {useState} from 'react';

import data from './data/schoolData';

import OneSchool from './components/OneSchool';
import Pagination from './components/Pagination';

import './App.css';

const App=()=> {
	const [allSchools, setAllSchools]=useState(data);
	//Keep track of the open Accordion
	const [defaultKey, setDefaultKey] =useState(0);

	// Pagination
	const [currentPage, setCurrentPage] = useState(1);
	const objsPerPage = 1;

	// Get current Keys
	const indexOfLastObj = currentPage * objsPerPage;
	const indexOfFirstObj = indexOfLastObj - objsPerPage;
	const allKeys =Object.keys(allSchools).filter(key=>key!=='undefined');
	const currentKeys = allKeys.slice(indexOfFirstObj, indexOfLastObj);

	// Change Page
	const paginate =pageNumber => {
		setDefaultKey(0);
		setCurrentPage(pageNumber);
	};
	return (
		<div className="App">
			
			{currentKeys.map(schoolKey => (
				<OneSchool	school={allSchools[schoolKey]} 
									schkey={schoolKey} 
									defaultKey ={defaultKey}
									setDefaultKey={setDefaultKey}
									allSchools ={allSchools}
									setAllSchools={setAllSchools}
				/>
			))}
		
			<div className="pageNums">
				<Pagination objsPerPage={objsPerPage} totalObjs={allKeys.length} paginate={paginate}/>
			</div>

		</div>
	);
}

export default App;
