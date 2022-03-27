import React, { useState } from 'react';
import TrackClient from '../clients/TrackClient';

import type {SyntheticEvent} from 'react';

export default function TrackImporter() {
    const [url, setUrl] = useState('');

    function onChange(event: SyntheticEvent) {
        const {value} = event.target as HTMLInputElement;
        setUrl(value);
    }

    function importTrack() {
        TrackClient.importTrack(url);
    }

    return (
        <div style={{display: 'flex'}}>
            <input
                style={{
                    textOverflow: 'ellipsis',
                    maxWidth: '300px'
                }}
                className="input"
                type="text"
                placeholder="Track
            url"
                value={url}
                onChange={onChange}
            />
            <button
                className='button is-success'
                onClick={importTrack}
            >
                Import
            </button>
        </div>
    )
}
