import React from 'react';

export class AdminView extends React.Component{
    
    people = [
        {name: 'chris'},
        {name: 'john'}
    ];

    constructor(props) {
        super(props);
    }

    render(){
        return(
            <div>
                <div>
                    { this.people.map(person => (
                        <p>
                            <button type="button" className="btn" >
                                Delete {person.name}
                             </button>
                        </p>
                    ))}
                </div>
            </div>
        );
    }
}