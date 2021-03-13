const myHeading = document.querySelector('h1');
myHeading.textContent = "THIS IS THE JAVA FILE";

import React from 'react';
import Header from './Login_Page'

function App() {
    return (
        <div className='container'>
            <Header />
        </div>
    )
}