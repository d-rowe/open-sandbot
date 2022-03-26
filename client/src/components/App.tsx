import React from 'react';
import SpeedSlider from './SpeedSlider';
import StopButton from './StopButton';
import TrackTable from './TrackTable';

function App() {
  return (
    <div className="App">
      <SpeedSlider/>
      <TrackTable/>
      <StopButton/>
    </div>
  );
}

export default App;
