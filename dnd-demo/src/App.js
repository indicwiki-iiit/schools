import React from 'react';

import Home from './components/Home';
import OneSchool from './components/OneSchool';
import {BrowserRouter as Router, Switch, Route, useHistory } from 'react-router-dom';

import './App.css';

const App=()=> {
	document.title='SUP'
	let history = useHistory();
	return (
		<div className="main">
			<Router><Switch>
				<Home exact path="/" component={Home} />
				<Route exact path="/uid=:uid" history={history} component={OneSchool} />
			</Switch></Router>
		
			{/* 
			<OneSchool	school={allSchools[schoolKey]} 
								schkey={schoolKey} 
								defaultKey ={defaultKey}
								setDefaultKey={setDefaultKey}
								allSchools ={allSchools}
								setAllSchools={setAllSchools}
			/> 
			*/}
				
		</div>
	);
}

export default App;
