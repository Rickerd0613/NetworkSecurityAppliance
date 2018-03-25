import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import logo from './logo.svg';
import './App.css';

import Home from './Home.js';
import Settings from './Settings.js';

class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <Route exact path="/" component={Home} />
          <Route path="/home" component={Home} />
          <Route path="/settings" component={Settings} />
        </div>
      </Router>
    );
  }
}

export default App;
