import BaseClient from './BaseClient';

const ENDPOINT = '/api/bot/';

const BotClient = {
    setSpeed(speed: number) {
        return post('speed', {speed});
    },

    stop() {
        return post('stop');
    },

    moveToAngles(angle1: number, angle2: number) {
        return post('move-to-angles', {angles: [angle1, angle2]});
    }
}

function post(relativeEndpoint: string, payload: Object = {}) {
    return BaseClient.post(ENDPOINT + relativeEndpoint, payload);
}

export default BotClient;
