import ApiClient from "./ApiClient";

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

export default {
    async getTracksMetadata() {
        return ApiClient.get('/api/tracks-metadata') as Promise<TracksMetadata>;
    },

    async startTrack(trackId: string): Promise<void> {
        const response = await ApiClient.post('/api/start-track', {trackId});
        if (response.status !== 201) {
            throw new Error(`Error starting track ${trackId}`);
        }
    }
}
