import React from 'react';
import { Link } from 'react-router-dom';
import Card from 'react-bootstrap/Card';

import data from '../data/schoolNames';

import '../css/Components.css'

const Home =()=>{

	return (
		<div className='homeSpace'>
			<div className='m-2'>
				<h1>Schools</h1>
			</div>
			<div className="allCards">
				{data.map(cur => (
					// <div className='Item'>
					<Link to={`/uid=${cur.value}`} className='Item'>
						<Card border='light' className='card'>
							<Card.Header className='cardHead' style={{'fontSize':'120%'}}>
								{cur.value}
							</Card.Header>
							<Card.Title className='cardTitle' style={{'fontSize':'150%'}}>
								{cur.label}
							</Card.Title>
						</Card>
					</Link>
					//</div>
				))}
			</div>
		</div>
	);
}

export default Home;