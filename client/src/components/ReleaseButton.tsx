import React from 'react';
import BotClient from '../clients/BotClient';

export default function ReleaseButton() {
    return (
        <button
            className='button is-primary'
            onClick={BotClient.release}
        >
            Release
        </button>
    )
}
