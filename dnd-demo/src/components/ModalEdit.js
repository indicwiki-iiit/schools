import React, { useState } from 'react';
import styled from 'styled-components'
import { ReactTransliterate } from "react-transliterate";
import { Button, Form, Modal } from "react-bootstrap";

import '../css/Components.css';
import "react-transliterate/dist/index.css";

const ModalEdit =(props) =>{
	const [text, setText] =useState(props.pair[1]);

	const applyChanges=()=>{
		props.modalUpdate(props.index, text);
		props.setModalShow(false);
	};

	return (
		<>
			<Modal {...props} size="lg" centered
				aria-labelledby="contained-modal-title-vcenter" >
				
				<Modal.Header closeButton>
					<Modal.Title id="contained-modal-title-vcenter">
						Editing {props.pair[0]}
					</Modal.Title>
				</Modal.Header>
				<Modal.Body>
					<ReactTransliterate
						lang="te"
						value={text}
						onChange={(e) => setText(e.target.value)}
						offsestX='10px' 
						offsetY='10px'
						Component='textarea'
						containerClassName ='editArea'
						activeItemStyles={{backgroundColor:'rgb(0,123,255)', fontSize:'170%'}}
					/>
				</Modal.Body>
				<Modal.Footer>
					<Button variant='danger' onClick={()=>props.setModalShow(false)}>Close</Button>
					<Button onClick={applyChanges}>Apply Changes !</Button>
				</Modal.Footer>
				
			</Modal>
		</>
	  );
}

export default ModalEdit;