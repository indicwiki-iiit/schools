import React, { useEffect, useState } from 'react';
import {useForm} from "react-hook-form";
import { Draggable } from "react-beautiful-dnd";
// import { ReactTransliterate } from "react-transliterate";
import { Accordion, Button, Card, Form, useAccordionToggle } from "react-bootstrap";

import ModalEdit from './ModalEdit';

import exclamation from '../data/exclamation.png';

import '../css/Components.css';
// import "react-transliterate/dist/index.css";

const CategoryList = ({schoolCats, setSchoolCats, generateArticle}) =>{
	const {register, handleSubmit} = useForm();
	const [modalShow, setModalShow] =useState(false);
	
	// const toggleModal =(index, bool)=>{
	// 	let newModal = [...modalShow];
	// 	newModal[index]=bool;
	// 	setModalShow(newModal);
	// }

	useEffect(() => {
		generateArticle(schoolCats)
   }, [schoolCats]);

	const modify = (data) => {
		var values = [...schoolCats];
		values.map((pair, index) =>{	
			if(index!==11){
				values[index][1] = data[pair[0]]
			}
		})
		console.log('@modify updated values:', values)

		setSchoolCats(values);
	};

	const modalUpdate =(i, value) =>{
		let values = [...schoolCats];
		values[i][1] =value;
		console.log("mUpdate:", values[i][1])
		setSchoolCats(values);
	}

	const CustomToggle =({children, eventKey, className}) =>{
		const decoratedOnClick =useAccordionToggle(eventKey, ()=>
			console.log('decoratedOnClick @', eventKey),
		);
		return (
			<Accordion.Toggle as={Card.Header} eventKey={eventKey}
				onClick={decoratedOnClick} className={className}>
				{children}

			</Accordion.Toggle>
		);
	};
	
	const Category =({pair, index}) =>{
		{console.log(pair[0], pair[1].length)}
		const curKey=(index.toString()+pair[0]).toString();
		return (
			<Draggable draggableId={pair[0]} index={index}>
				{provided => (
					<Card ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
						<CustomToggle eventKey={pair[0]} className='otherHeading'>{pair[0]}</CustomToggle>
						<Accordion.Collapse eventKey={pair[0]}>
							<Form onSubmit={handleSubmit(modify)}>
								<Form.Control size="lg" as="textarea" rows={3}
													index ={index}
													name={curKey}
													{...register(pair[0])}
													aria-describedby={curKey} 
													defaultValue={pair[1]}
													placeholder={`Please add some details about the school's ${pair[0]}`}
													// onChange={e=>update(e, index)}

													style={{fontSize:'140%'}}
								/>
								<div className="keepRight">
									<Button type="submit">Apply Changes !</Button>
								</div>
							</Form>
						</Accordion.Collapse>
					</Card>
				)}
			</Draggable>
		);
	};

	const References =({pair, index}) =>{
		const curKey=(index.toString()+pair[0]).toString();
		return (
			<Card>
				<CustomToggle eventKey={pair[0]} className='refHeading'>{pair[0]}</CustomToggle>
				<Accordion.Collapse eventKey={pair[0]}>
					<>
						<Form>
							<Form.Control size="lg" as="textarea" rows={3}
												readOnly
												index ={index}
												name={curKey}
												aria-describedby={curKey} 
												defaultValue={pair[1]}
												placeholder={`Please add some details about the school's ${pair[0]}`}
												// onChange={event=>modify(index, event)}
							/>
							<div className="keepRight">
								<Button onClick={()=>setModalShow(true)}>Edit</Button>
							</div>
						</Form>

						<ModalEdit
							pair ={pair}
							index={index}
							show ={modalShow}
							modalUpdate={modalUpdate}
							setModalShow ={setModalShow}
						/>
					</>
				</Accordion.Collapse>
			</Card>
				
		);
	};

	return(
		<div style={{padding:'15px', backgroundColor:'lightgray'}}>
			<Accordion>
				{schoolCats.map((pair, index) => (
					<>
						{pair[0]!=='References' &&
						<Category pair={pair} index={index} key={`${index}-${pair[0]}`} />}
						
						{pair[0]==='References' &&
						<References pair={pair} index={index} key={`${index}-${pair[0]}`} /> }
					</>
				))}
			</Accordion>
		</div>
	);
};

export default CategoryList;