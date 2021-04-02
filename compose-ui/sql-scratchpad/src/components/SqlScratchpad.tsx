import axios from 'axios';
import React from 'react';

import hueComponents from 'gethue/lib/components/QueryEditorWebComponents';
import hueConfig from 'gethue/lib/config/hueConfig';
import Executor from 'gethue/lib/execution/executor';
import SqlExecutable from 'gethue/apps/editor/execution/sqlExecutable';

import { QueryEditor } from './QueryEditor';
import { ExecuteButton } from './ExecuteButton';
import { ExecuteProgress } from './ExecuteProgress';
import { ResultTable } from './ResultTable';
import {ExecuteLimit} from "./ExecuteLimit";

const API_URL = 'http://localhost:8005'

axios.defaults.baseURL = API_URL;



hueComponents.configure({
  baseUrl: API_URL
});

interface SqlScratchpadState {
  activeExecutable?: SqlExecutable;
  executor?: Executor;
}

type KnockoutObservable<T> = () => T;

export class SqlScratchpad extends React.Component<{}, SqlScratchpadState> {
  state = {
    activeExecutable: undefined,
    executor: undefined
  }

  constructor(props: {}) {
    super(props);
    this.setActiveExecutable = this.setActiveExecutable.bind(this);
  }

  componentDidMount() {
    console.info('Refreshing config');
    const _this = this;

    axios.post('iam/v1/get/auth-token/', {username: "hue", password: "hue"}).then(function(data) {
      console.log(data['data']);

      axios.post('iam/v1/verify/auth-token/', {token: data['data']['token']});

      axios.defaults.headers.common['Authorization'] = 'JWT ' + data['data']['token'];
    }).then(function() {
      //axios.post('/desktop/api2/get_config')
      hueComponents.refreshConfig()
      .then(() => {
        const connector = hueConfig.findEditorConnector(() => true); // Returns the first connector

        _this.setState({
          executor: hueComponents.createExecutor({
            compute: (() => ({ id: 'default' })) as KnockoutObservable<any>,
            connector: (() => connector) as KnockoutObservable<any>,
            database: (() => 'default') as KnockoutObservable<any>,
            namespace: (() => ({ id: 'default' })) as KnockoutObservable<any>,
          })
        })
      }).catch(() => {
        console.warn('Failed loading the Hue config')
      })
    });
  }

  setActiveExecutable(activeExecutable: SqlExecutable) {
    this.setState({
      activeExecutable
    })
  }

  render() {
    const executor = this.state.executor;
    if (executor) {
      return <React.Fragment>
        <div className="ace-editor">
          <QueryEditor executor={executor} setActiveExecutable={this.setActiveExecutable} />
        </div>
        <div className="executable-progress-bar">
          <ExecuteProgress activeExecutable={this.state.activeExecutable} />
        </div>
        <div className="executable-actions">
          <ExecuteButton activeExecutable={this.state.activeExecutable} />
          <ExecuteLimit activeExecutable={this.state.activeExecutable} />
        </div>
        <div className="result-table">
          <ResultTable activeExecutable={this.state.activeExecutable} />
        </div>
      </React.Fragment>
    } else {
      return <div>Loading Config...</div>
    }
  }
}
