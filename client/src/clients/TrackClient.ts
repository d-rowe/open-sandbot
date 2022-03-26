import BaseClient from './BaseClient';

type SingleTrackMetadata = {
    name: string,
    track_id: string,
    created: string,
}

export type TracksMetadata = {
    created: string,
    updated: string,
    tracks: SingleTrackMetadata[]
};

const TrackClient = {
    async getTracksMetadata() {
        return BaseClient.get('/api/tracks-metadata') as Promise<TracksMetadata>;
    },

    async startTrack(trackId: string) {
        await BaseClient.post('/api/start-track', {trackId});
    },

    async importTrack(trackUrl: string) {
        await BaseClient.post('/api/import-track', {url: trackUrl});
    }
}

export default TrackClient;
