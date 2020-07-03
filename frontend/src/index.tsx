import { SocketClient } from 'app/common/api/sockets';
import store from 'app/common/store/configureStore';
// connect icons font
import 'assets/icomoon/style.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './app/App';

import './index.scss';

import * as serviceWorker from './serviceWorker';

import './types.d.ts';

export const socket = new SocketClient();

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
