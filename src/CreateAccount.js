import React from 'react';
export class CreateAccount extends React.Component{

    constructor(props) {
        super(props);
    }

    render(){
        return(
          <div className="CreateAccount">
                <div className="form">
                    <div className="form-group">
                        <label htmlFor="username">Enter username: </label>
                        <input type="text" name="username" placeholder="username"/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Enter password: </label>
                        <input type="text" name="password" placeholder="password"/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Confirm password: </label>
                        <input type="text" name="password" placeholder="password"/>
                    </div>
                </div>
                <div className="footer">
                    <button type="button" className="btn">
                        Create Account
                    </button>
                </div>
            </div>
        );
    }
}