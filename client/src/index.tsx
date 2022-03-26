import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './components/App';
import TrackClient from './clients/TrackClient';

// @ts-ignore
window.trackClient = TrackClient;

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
