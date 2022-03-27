import React from 'react';
import SpeedSlider from './SpeedSlider';
import StopButton from './StopButton';
import TrackImporter from './TrackImporter';
import TrackTable from './TrackTable';

function App() {
  return (
    <div className="App">
      <SpeedSlider/>
      <TrackTable/>
      <StopButton/>
      <TrackImporter/>
    </div>
  );
}

export default App;
