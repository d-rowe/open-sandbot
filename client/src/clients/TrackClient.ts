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
        return get('metadata') as Promise<TracksMetadata>;
    },

    async startTrack(trackId: string) {
        await post('start', {trackId});
    },

    async importTrack(trackUrl: string) {
        await post('import', {url: trackUrl});
    }
}

function get(resource: string) {
    return BaseClient.get(getResourceEndpoint(resource));
}

function post(resource: string, payload: Object = {}) {
    return BaseClient.post(getResourceEndpoint(resource), payload);
}

function getResourceEndpoint(resource: string): string {
    return '/api/tracks/' + resource;
}

export default TrackClient;
