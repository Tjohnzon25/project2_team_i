import './App.css';
import { CreateAccount } from './CreateAccount.js';
import { AdminView } from './AdminView.js';
import {Route} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Route exact path="/" component={CreateAccount}/>
      <Route exact path="/AdminView" component={AdminView}/>
    </div>
  );
}

export default App;
