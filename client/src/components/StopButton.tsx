import React from 'react';
import BotClient from '../clients/BotClient';

export default function StopButton() {
    return (
        <button
            className='button is-danger'
            onClick={BotClient.stop}
        >
            Stop
        </button>
    )
}
