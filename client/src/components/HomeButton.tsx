import React from 'react';
import BotClient from '../clients/BotClient';

export default function HomeButton() {
    return (
        <button
            className='button is-danger'
            onClick={BotClient.setHome}
        >
            Set Home
        </button>
    )
}
