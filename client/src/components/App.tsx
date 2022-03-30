import React from 'react';
import SpeedSlider from './SpeedSlider';
import StopButton from './StopButton';
import ReleaseButton from './ReleaseButton';
import HomeButton from './HomeButton';
import TrackImporter from './TrackImporter';
import TrackTable from './TrackTable';

function App() {
  return (
    <div className="App">
      <SpeedSlider/>
      <TrackTable/>
      <StopButton/>
      <ReleaseButton/>
      <HomeButton/>
      <TrackImporter/>
    </div>
  );
}

export default App;
