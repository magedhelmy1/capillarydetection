import React from 'react';
import './App.css';
import Classifier from './components/Classifier/Classifier';
import Navigation from './components/Navigation/Navigation';
import Info from './components/Info/Info';
import {BrowserRouter, Route, Switch} from 'react-router-dom'


function App() {
    return (
        <BrowserRouter>
            <Navigation/>
            <div className='App'>
                <Switch>
                    <Route exact path='/' component={Classifier}/>
                    <Route exact path='/info' component={Info}/>
                    <Route exact path='*' component={Classifier}/>
                </Switch>
            </div>
        </BrowserRouter>
    );
}

export default App;
