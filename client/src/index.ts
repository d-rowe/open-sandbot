import KeyboardShortcuts from './KeyboardShortcuts';
import Logger from './Logger';
import SandBotClient from './SandBotClient';
import TrackClient from './TrackClient';
import Tracks from './Tracks';

window.onload = hydrate;
window.sandbot = SandBotClient;

async function hydrate() {
    Tracks.init();
    TrackClient.getTracksMetadata().then(Tracks.loadTracksMetada);

    addClickHandler('software-update', SandBotClient.softwareUpdate);

    KeyboardShortcuts.on('Space', SandBotClient.home);
    KeyboardShortcuts.on('ArrowLeft', SandBotClient.lowerArmLeft);
    KeyboardShortcuts.on('ArrowRight', SandBotClient.lowerArmRight);
    KeyboardShortcuts.on('ArrowUp', SandBotClient.upperArmLeft);
    KeyboardShortcuts.on('ArrowDown', SandBotClient.upperArmRight);
    KeyboardShortcuts.on('Backspace', Logger.clear);
}

function addClickHandler(id: string, handler: () => void) {
    document.getElementById(id).addEventListener('click', handler);
}
