import React from 'react';
export class AdminView extends React.Component{
    
    people = [
        {name: 'samson', id: 0},
        {name: 'john', id: 1},
        {name: 'martha', id: 2},
        {name: "mary", id: 3}
    ];

    removeUser = (p) =>{
        console.log(typeof p)
        var i;
        for(i = 0; i < this.people.length; i++){
            if( i === p){
                break;
            }
        }
        this.people.splice(i, 1);
        console.log('people size is ' + this.people.length + ' removed is ' + p + ' uniqueid is ' + i);
        this.refreshPage();
    }

    refreshPage = () =>{
        window.location.reload(true);   
    }

    render(){
        return(
            <div>
                <div>   
                    { this.people.map(person => (
                        <p>
                            {console.log(typeof person.id)}
                            <button type="button" className="btn"  onClick={() => this.removeUser(person.id)}  >
                                Delete {person.name} 
                             </button>
                        </p>
                    ))}
                </div>
            </div>
        );
    }
}