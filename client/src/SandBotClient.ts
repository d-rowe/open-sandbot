import ApiClient from './ApiClient';
import Logger from './Logger';

const ENDPOINT = '/api/bot/';

function post(relativeEndpoint: string, payload: Object) {
    return ApiClient.post(ENDPOINT + relativeEndpoint, payload);
}

export default {
    async softwareUpdate() {
        Logger.info('Software update started');
        const response = await fetch('/api/software-update', {method: 'POST'});
        if (response.status !== 201) {
            Logger.error('Software update failed');
            return;
        }

        Logger.info('Software update succeeded');
    },

    moveToAngles(angle1: number, angle2: number) {
        return post('move-to-angles', {angles: [angle1, angle2]});
    }
}
