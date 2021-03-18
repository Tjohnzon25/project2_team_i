import React,{useState, useEffect} from 'react';
import { Item } from '../Components/Item/item'

export const Wishlist = ()=>{

	const [item, setItem] = useState([])

	useEffect(()=>{
		fetch('/api').then(response =>{ //need to add a fetch directory...where is fetch going to get the data from
			if(response.ok){
				return response.json()
			}
		}).then(data => console.log(data))
	}, [])

	return(
		<>
			<Item/>
		</>
	)
}