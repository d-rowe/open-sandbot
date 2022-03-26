import React from 'react';
import debounce from 'debounce';
import BotClient from '../clients/BotClient';

import type { SyntheticEvent } from 'React';

const commitSpeed = debounce(BotClient.setSpeed, 150);

function SpeedSlider() {
    function onChange(event: SyntheticEvent) {
        const {value} = event.target as HTMLInputElement;
        const speed = Number(value);
        commitSpeed(speed)
    }

    return (
        <div style={{display: 'flex'}}>
            <label style={{marginRight: '8px'}}>Speed</label>
            <input
                type="range"
                min="0"
                max="100"
                defaultValue="100"
                className="speed-slider"
                onChange={onChange}
            />
        </div>
    )
}

export default SpeedSlider;
