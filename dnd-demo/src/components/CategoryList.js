import React from 'react';
// import {useForm} from "react-hook-form";
import { Draggable } from "react-beautiful-dnd";
import { Accordion, Button, Card, Form, useAccordionToggle } from "react-bootstrap";

const CategoryList = ({curSchool, setCurSchool, defaultKey, setDefaultKey}) =>{

	// const {register, handleSubmit} = useForm();

	const modify = (index, event) => {
		event.preventDefault();
		const values = [...curSchool];
		
		values[index][1] = event.target.value;
	
		setCurSchool(values);
	};

	const CustomToggle =({children, eventKey}) =>{
		const decoratedOnClick =useAccordionToggle(eventKey, ()=>
			console.log('decoratedOnClick @', eventKey),
		);

		setDefaultKey(eventKey);

		return (
			<Accordion.Toggle as={Card.Header} eventKey={eventKey}
				onClick={decoratedOnClick}>
				{children}
			</Accordion.Toggle>
		);
	};

	const Category =({pair, index}) =>{
		if(['code', 'title'].includes(pair[0])){
			return (<></>);
		} else {
			const curKey=index.toString()+pair[0];
			return (
				<Draggable draggableId={pair[0]} index={index}>
					{provided => (
						<Card ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
							<CustomToggle eventKey={pair[0]}>{pair[0]}</CustomToggle>
							<Accordion.Collapse eventKey={pair[0]}>
								{/* <Form.Control as="textarea" rows={3}
									id={curKey}
									name={curKey}
									aria-describedby={curKey}
									
									placeholder="Feel free to add any relevant details"
									value={pair[1]}
									onChange={(event) => modify(index, event)}			
								/> */}
								<Form onSubmit={event=>modify(index, event)}>
									<Form.Control as="textarea" rows={3}
														name={curKey}
														aria-describedby={curKey} 
														defaultValue={pair[1]}
														placeholder="Feel free to add any relevant details"
														// onChange={event=>modify(index, event)}
									/>
									<div className="KeepRight">
										<Button size="sm" type="submit">Apply Changes !</Button>
									</div>
								</Form>

							</Accordion.Collapse>
						</Card>
					)}
				</Draggable>
			);
		}
	};

	return(
		<Accordion defaultActiveKey={defaultKey}>
			{curSchool.map((pair, index) => (
				<Category pair={pair} index={index} key={`${index}-${pair[0]}`} />
			))}
		</Accordion>
	);
};

export default CategoryList;