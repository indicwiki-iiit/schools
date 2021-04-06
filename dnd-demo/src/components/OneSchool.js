import React, {useState, useEffect} from 'react';
import ResizePanel, { AsyncMode } from 'react-resize-panel';
import { DragDropContext, Droppable } from "react-beautiful-dnd";

import CategoryList from './CategoryList';


const OneSchool =({school, schKey, defaultKey, setDefaultKey, allSchools, setAllSchools}) =>{
	const [title, setTitle] =useState('');
	const [curSchool, setCurSchool]=useState(school);
	const [curArticle, setCurArticle]=useState('');

	useEffect(()=>{
		console.log("useEffect @ OneSchool")
		// Update the article
		updateAll(curSchool);
		// Update all schools data
		var newSchools =allSchools;
		newSchools[schKey]=curSchool;
		setAllSchools(newSchools);
	}, [curSchool, schKey, allSchools])

	const updateAll =curSchool =>{
		var article ='';
		curSchool.forEach((category, index) =>{
			if (category[0]==='title') {
				setTitle(category[1]);
			}
			else if(!['code', 'title'].includes(category[0])){
				article=article+category[1];
			}
		});
		setCurArticle(article);
	};

	const onDragEnd =(result) =>{
		console.log(result);
		setCurSchool(curSchool);
		// const {destination, source, draggableId} =result;

		// if (!destination){
		// 	return;
		// }
		// else if (destination.index===source.index){
		// 	return;
		// }

		// const newOrder =Array.from(curSchool);
		// newOrder.splice(source.index, 1);
		// newOrder.splice(destination.index, 0, curSchool[source.index]);
		
		// setCurSchool(newOrder);
		// console.log(curSchool);
	};

	return(
		<div classname='container'>

			<div className='header'>
				{title}
			</div>

			<div className='body'>

				<ResizePanel direction="e" style={{ flexGrow: '1' }} >
					<div className='sideContent'>
						<DragDropContext  onDragEnd={onDragEnd}>
							<Droppable droppableId='list'>
								{provided => (
								<div ref={provided.innerRef} {...provided.droppableProps}>

									<CategoryList curSchool={curSchool} setCurSchool={setCurSchool}
														defaultKey={defaultKey} setDefaultKey={setDefaultKey}/>

									{provided.placeholder}
								</div>
								)}
							</Droppable>
						</DragDropContext>
					</div>
				</ResizePanel>

				<div className='article'>{curArticle}</div>

			</div>

		</div>
	);
}


export default OneSchool;