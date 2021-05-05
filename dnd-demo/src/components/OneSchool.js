import React, {useState, useEffect} from 'react';
import { Alert, Button, Modal } from "react-bootstrap";
import ResizePanel from 'react-resize-panel';
import { DragDropContext, Droppable } from "react-beautiful-dnd";

import CategoryList from './CategoryList';

import '../css/Components.css';

const OneSchool =({ match, history }) =>{
	console.log('match:', match)
	console.log('history', history)
	const [done, setDone]=useState(false);
	
	// Alert's Toggles
	const [showInfo, setShowInfo] = useState(false);
	const [showSuccess, setShowSuccess] = useState(false);

	const [title, setTitle] =useState('');
	const [schoolCats, setSchoolCats]=useState([]);
	const [article, setArticle]=useState('');

	const generateArticle =(schoolCats)=>{
		var article = '';
		schoolCats.map((pair) => {
			article = article.concat(pair[1])
			return null;
		});
		setArticle(article);
   }

	useEffect(() => {
		setDone(false);
		const postObj = {
			method: 'POST',
			cache: 'no-cache',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({udiseCode: Number(match.params.uid)})
		};
		const getDetails =async () => {
			console.log('API-URL',process.env.REACT_APP_API)
			const response = await fetch(process.env.REACT_APP_API+'/get_schoolData', postObj);
			const data = await response.json();
			setTitle(data.title);
			setSchoolCats(data.schoolCats);
			generateArticle(data.schoolCats);
			setDone(true);
		};

		getDetails();
   }, [match.params.uid]);

	const saveChanges =() =>{
		console.log('SAVE CHANGES');
		// setShowInfo(true);
		const postObj = {
			method: 'POST',
			cache: 'no-cache',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({ udiseCode: Number(match.params.uid), schoolCats: schoolCats })
		};
		const saveDetails =async () => {
			console.log('API-URL',process.env.REACT_APP_API)
			const response = await fetch(process.env.REACT_APP_API+'/save_schoolCats', postObj);
			const data = await response.json();
			setShowSuccess(data.show);
		};

		saveDetails();
	};

	const reorder = (list, startIndex, endIndex) => {
		const result = Array.from(list);
		const [removed] = result.splice(startIndex, 1);
		result.splice(endIndex, 0, removed);
	  
		return result;
	};
	
	const onDragEnd =(result) =>{
		if (!result.destination) {
			return;
		}  
		if (result.destination.index === result.source.index) {
			return;
		}
		const newCats = reorder(
			schoolCats,
			result.source.index,
			result.destination.index
		);
	  
		setSchoolCats(newCats);
	};

	const goHome=()=>{
		history.push('/');
		setShowSuccess(false);
	};

	if(!done){
		return(<h1>Loading...</h1>)
	}
	if(done && title===''){
		return(<h1>No School found with UDSE Code {match.params.uid}</h1>)
   }

	return(
		<div classname='container'>

			<div className='header'>
				{title}
			</div>

			<div className="alertsArea">
				{/* <Alert show={showInfo} variant="primary" className='alert'
						onClose={() => setShowInfo(false)} dismissible>
					<Alert.Heading>Your changes are being saved !</Alert.Heading>
					<p>
						<b style={{color:'red'}}>Please wait</b> till you get notified that your changes 
						saved properly.
					</p>
				</Alert> */}
				<Modal show={showSuccess} onHide={()=>setShowSuccess(false)}>
					<Modal.Header closeButton>
						<Modal.Title>Done !</Modal.Title>
					</Modal.Header>
					<Modal.Body>
						<Alert  variant="success" className='alert'>
							<Alert.Heading>
								Your changes are saved !
								<p></p>
								<p>
									<b>Thank you</b> for your contribution !
								</p>
							</Alert.Heading>
						</Alert>
					</Modal.Body>
					<Modal.Footer>
						<Button variant="primary" onClick={goHome}>
							Home
						</Button>
						<Button variant="secondary" onClick={()=>setShowSuccess(false)}>
							Close
						</Button>
					</Modal.Footer>
				</Modal>
			</div>

			<div className='body'>

				<ResizePanel direction="e" style={{ flexGrow: '3' }} >
					<div className='sideContent'>
						<DragDropContext  onDragEnd={onDragEnd}>
							<Droppable droppableId='list'>
								{provided => (
								<div ref={provided.innerRef} {...provided.droppableProps}>

									<CategoryList schoolCats={schoolCats} setSchoolCats={setSchoolCats} generateArticle={generateArticle}/>

									{provided.placeholder}
								</div>
								)}
							</Droppable>
						</DragDropContext>
					</div>
				</ResizePanel>

				<div className='article'>
					{article.split('\n').map(line=><div>{line}</div>)}
				</div>

			</div>
			
			<div className='footButtons'>
				<Button size='lg' href='/' variant='primary'>Home</Button>
				<Button size='lg' onClick={saveChanges} variant='primary'>Save Changes</Button>
			</div>
		</div>
	);
}


export default OneSchool;