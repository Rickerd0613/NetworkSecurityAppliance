import React from "react";
import AppHeader from './AppHeader';
import {Panel, Button} from 'react-bootstrap';

export default class Settings extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      whitelist: whitelist.join(', '),
      blacklist: blacklist.join(', '),
      ruletype: 'suricata',
      rulepath: '',
      honeypotpath: '',
    };

    this.onWhiteListChange = this.onWhiteListChange.bind(this);
    this.onBlackListChange = this.onBlackListChange.bind(this);
    this.onRuleTypeChange = this.onRuleTypeChange.bind(this);
    this.onHoneyPotPathChange = this.onHoneyPotPathChange.bind(this);
    this.onRulePathChange = this.onRulePathChange.bind(this);
    this.onSaveClick = this.onSaveClick.bind(this);
    this.getData = this.getData.bind(this);
  }
  onWhiteListChange(event) {
    this.setState({
      whitelist: event.target.value,
    });
  }
  onBlackListChange(event) {
    this.setState({
      blacklist: event.target.value,
    });
  }
  onRuleTypeChange(event) {
    this.setState({
      ruletype: event.target.value,
    });
  }
  onHoneyPotPathChange(event) {
    this.setState({
      honeypotpath: event.target.value,
    });
  }
  onRulePathChange(event) {
    this.setState({
      rulepath: event.target.value,
    });
  }
  onSaveClick() {
    console.log('save click');
    const toSubmit = {
      whitelist: this.state.whitelist.split(', '),
      blacklist: this.state.blacklist.split(', '),
      ruletype: this.state.ruletype,
      rulepath: this.state.rulepath,
      honeypotpath: this.state.honeypotpath,
    }

    console.log(toSubmit);
    fetch('/config', {
      method: 'post',
      body: JSON.stringify(toSubmit),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
    })
  }

  getData = () => {
    fetch('/config')
    .then(results => {
      return results.json();
    }).then(responseData => {
      this.setState({
        whitelist: responseData.whitelist.join(', '),
        blacklist: responseData.blacklist.join(', '),
        ruletype: responseData.ruletype,
        rulepath: responseData.rulepath,
        honeypotpath: responseData.honeypotpath,
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
          <Panel className="list-panel">
            <Panel.Heading>Whitelisted IPs</Panel.Heading>
            <Panel.Body><input
              type='text'
              onChange={this.onWhiteListChange}
              className="ip-input"
              value={this.state.whitelist}
            />
            </Panel.Body>
          </Panel>
          <Panel className="list-panel">
            <Panel.Heading>Blacklisted IPs</Panel.Heading>
            <Panel.Body><input
              type='text'
              onChange={this.onBlackListChange}
              className="ip-input"
              value={this.state.blacklist}
              />
            </Panel.Body>
          </Panel>
          <Panel className="list-panel">
            <Panel.Heading>Rule Type</Panel.Heading>
            <Panel.Body><select defaultValue="suricata">
              <option value="suricata">suricata</option>
            </select>
            </Panel.Body>
          </Panel>
          <Panel className="list-panel">
            <Panel.Heading>Honey Pot Log Path</Panel.Heading>
            <Panel.Body><input
              type='text'
              onChange={this.onHoneyPotPathChange}
              className="ip-input"
              value={this.state.honeypotpath}
              />
            </Panel.Body>
          </Panel>
          <Panel className="list-panel">
            <Panel.Heading>Rule File Path</Panel.Heading>
            <Panel.Body><input
              type='text'
              onChange={this.onRulePathChange}
              className="ip-input"
              value={this.state.rulepath}
              />
            </Panel.Body>
          </Panel>
          <Button
            className="save-button"
            bsStyle="primary"
            onClick={this.onSaveClick}>Save</Button>
        </div>
      </div>
    );
  }
}

const whitelist = [];

const blacklist = [];
