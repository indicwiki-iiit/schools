import React from 'react';

import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';

const Pagination =({objsPerPage, totalObjs, paginate}) => {

	const pageNumbers = [];

	for(let i=1; i<=Math.ceil(totalObjs/objsPerPage); i++){
		pageNumbers.push(i);
	}

	return (
		<>
		<ButtonGroup>
			{pageNumbers.map(number => (
				<Button onClick={() => paginate(number)}  key={number} href="#">
					{number}
				</Button>
			))}
		</ButtonGroup>
	   </>
	)
}

export default Pagination