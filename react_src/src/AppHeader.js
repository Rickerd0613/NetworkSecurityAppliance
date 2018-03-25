import React from "react";
import Home from "./Home";
import {BrowserRouter as Route, Link} from 'react-router-dom';
import {Navbar, Nav, NavItem} from 'react-bootstrap';

export default class AppHeader extends React.Component {
  render () {
    return (
      <Navbar>
        <Nav>
          <NavItem eventKey={1} href="/home">
            Home
          </NavItem>
          <NavItem eventKey={2} href="/settings">
            Settings
          </NavItem>
        </Nav>
      </Navbar>
    );
  }
}
