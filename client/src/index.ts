import SandBotClient from "./SandBotClient";

window.onload = hydrate;

function hydrate() {
    document.querySelector('#movement-home').addEventListener('click', SandBotClient.home);
    document.querySelector('#movement-lower-arm-left').addEventListener('click', SandBotClient.lowerArmLeft);
    document.querySelector('#movement-lower-arm-right').addEventListener('click', SandBotClient.lowerArmRight);
    document.querySelector('#movement-upper-arm-left').addEventListener('click', SandBotClient.upperArmLeft);
    document.querySelector('#movement-upper-arm-right').addEventListener('click', SandBotClient.upperArmRight);
}
