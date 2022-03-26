import React, { PureComponent } from 'react';
import TrackClient from '../../clients/TrackClient';

import type { TracksMetadata } from '../../clients/TrackClient';

type Props = {};
type State = {
    tracksMetadata?: TracksMetadata,
};

export default class TrackTable extends PureComponent<Props, State> {
    state: State = {};

    async componentDidMount() {
        const tracksMetadata = await TrackClient.getTracksMetadata();
        this.setState({ tracksMetadata });
    }

    render() {
        const { tracksMetadata } = this.state;
        if (!tracksMetadata) {
            return <h2>Loading tracks...</h2>
        }
        return (
            <table className='table'>
                <tbody>
                    {tracksMetadata.tracks.map(track => (
                        <tr>
                            <td style={{paddingRight: '8px'}}>{track.name}</td>
                            <td>
                                <button
                                    className='button'
                                    onClick={() => TrackClient.startTrack(track.track_id)}
                                >
                                    {">"}
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        )
    }
}
