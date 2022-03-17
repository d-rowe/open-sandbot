import KeyboardShortcuts from './KeyboardShortcuts';
import Logger from './Logger';
import SandBotClient from './SandBotClient';
import TrackClient from './TrackClient';
import Tracks from './Tracks';

window.onload = hydrate;

async function hydrate() {
    let angle1 = 0;
    let angle2 = 0;
    let inProgress = false;
    Tracks.init();
    TrackClient.getTracksMetadata().then(Tracks.loadTracksMetada);

    addClickHandler('software-update', SandBotClient.softwareUpdate);

    KeyboardShortcuts.on('Space', () => SandBotClient.moveToAngles(0, 0));
    KeyboardShortcuts.on('ArrowLeft', () => SandBotClient.moveToAngles(angle1 - 22.5, angle2));
    KeyboardShortcuts.on('ArrowLeft', () => SandBotClient.moveToAngles(angle1 + 22.5, angle2));
    KeyboardShortcuts.on('ArrowUp', () => SandBotClient.moveToAngles(angle1, angle2 - 22.5));
    KeyboardShortcuts.on('ArrowUp', () => SandBotClient.moveToAngles(angle1, angle2 + 22.5));
    KeyboardShortcuts.on('Backspace', Logger.clear);

    async function moveBy(a1Diff: number, a2Diff: number) {
        if (inProgress) {
            return;
        }
        inProgress = true;
        const a1Target = angle1 + a1Diff;
        const a2Target = angle2 + a2Diff;
        await SandBotClient.moveToAngles(angle1 + a1Diff, angle2 + a2Diff);
        angle1 = a1Target;
        angle2 = a2Target;
        inProgress = false;
    }
}

function addClickHandler(id: string, handler: () => void) {
    document.getElementById(id).addEventListener('click', handler);
}
