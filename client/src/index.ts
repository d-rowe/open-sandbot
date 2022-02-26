import KeyboardShortcuts from './KeyboardShortcuts';
import Logger from './Logger';
import SandBotClient from './SandBotClient';

window.onload = hydrate;

function hydrate() {
    addClickHandler('movement-home', SandBotClient.home);
    addClickHandler('movement-lower-arm-left', SandBotClient.lowerArmLeft);
    addClickHandler('movement-lower-arm-right', SandBotClient.lowerArmRight);
    addClickHandler('movement-upper-arm-left', SandBotClient.upperArmLeft);
    addClickHandler('movement-upper-arm-right', SandBotClient.upperArmRight);

    addClickHandler('software-update', SandBotClient.softwareUpdate);

    KeyboardShortcuts.on('Space', SandBotClient.home);
    KeyboardShortcuts.on('ArrowLeft', SandBotClient.lowerArmLeft);
    KeyboardShortcuts.on('ArrowRight', SandBotClient.lowerArmRight);
    KeyboardShortcuts.on('ArrowUp', SandBotClient.upperArmLeft);
    KeyboardShortcuts.on('ArrowDown', SandBotClient.upperArmRight);

    KeyboardShortcuts.on('Backspace', Logger.clear);
}

function addClickHandler(id: string, handler: () => void) {
    document.querySelector(`#${id}`).addEventListener('click', handler);
}
