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
    KeyboardShortcuts.on('ArrowLeft', () => moveBy(-22.5, 0));
    KeyboardShortcuts.on('ArrowRight', () => moveBy(22.5, 0));
    KeyboardShortcuts.on('ArrowDown', () => moveBy(0, -22.5));
    KeyboardShortcuts.on('ArrowUp', () => moveBy(0, 22.5));
    KeyboardShortcuts.on('Backspace', Logger.clear);

    async function moveBy(a1Diff: number, a2Diff: number) {
        if (inProgress) {
            return;
        }
        inProgress = true;
        const a1Target = angle1 + a1Diff;
        const a2Target = angle2 + a2Diff;
        Logger.info(`Moving to angles: ${a1Target}, ${a2Target}`)
        await SandBotClient.moveToAngles(a1Target, a2Target);
        angle1 = a1Target;
        angle2 = a2Target;
        inProgress = false;
    }
}

function addClickHandler(id: string, handler: () => void) {
    document.getElementById(id).addEventListener('click', handler);
}
