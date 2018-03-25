import React from "react";
import AppHeader from './AppHeader';
import {Panel} from 'react-bootstrap';
import _ from 'lodash';

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      data: null,
    };
    this.getData = this.getData.bind(this);
  }

  getData = () => {
    fetch('/profiles')
    .then(results => {
      return results.json();
    }).then(responseData => {
      this.setState({
        data: responseData,
      })
    })
  }

  componentDidMount() {
    this.getData();
  }

  render () {
    return (
      <div>
        <AppHeader />
        <div>
          {this.state.data && _.map(this.state.data, (value, key) => {
            return (
              <Panel className="list-panel">
                <Panel.Heading>{key}</Panel.Heading>
                <b><Panel.Body>Initial</Panel.Body></b>
                  <p className="ip-list">{value.initial.join(', ', (ip) => {
                    return (ip);
                  })}</p>
                <b><Panel.Body>New</Panel.Body></b>
                  <p className="ip-list">{value.new.join(', ', (ip) => {
                    return (ip);
                  })}</p>
              </Panel>
            );
          })}
        </div>
      </div>
    );
  }
}
