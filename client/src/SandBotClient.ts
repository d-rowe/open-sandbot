import ApiClient from './ApiClient';
import Logger from './Logger';

enum COMMANDS {
    HOME = 'HOME',
    ARM_LOWER_LEFT = 'ARM_LOWER_LEFT',
    ARM_LOWER_RIGHT = 'ARM_LOWER_RIGHT',
    ARM_UPPER_LEFT = 'ARM_UPPER_LEFT',
    ARM_UPPER_RIGHT = 'ARM_UPPER_RIGHT',
}

export default {
    async home(): Promise<void> {
        return sendMoveCommand(COMMANDS.HOME);
    },

    async lowerArmLeft() {
        return sendMoveCommand(COMMANDS.ARM_LOWER_LEFT);
    },

    async lowerArmRight() {
        return sendMoveCommand(COMMANDS.ARM_LOWER_RIGHT);
    },

    async upperArmLeft() {
        return sendMoveCommand(COMMANDS.ARM_UPPER_LEFT);
    },

    async upperArmRight() {
        return sendMoveCommand(COMMANDS.ARM_UPPER_RIGHT);
    },

    async softwareUpdate() {
        Logger.info('Software update started');
        const response = await fetch('/api/software-update', {method: 'POST'});
        if (response.status !== 201) {
            Logger.error('Software update failed');
            return;
        }

        Logger.info('Software update succeeded');
    },

    async moveToAngles(angle1: number, angle2: number) {
        await ApiClient.post('/api/move-to-angles', {angles: [angle1, angle2]});
    }
}

async function sendMoveCommand(command: string): Promise<void> {
    const response = await fetch(
        `/api/move`,
        {
            method: 'POST',
            body: JSON.stringify({ command })
        }
    );
    if (response.status !== 201) {
        Logger.error(`Command failed: ${command}`);
        return;
    }

    Logger.info(`Command sent: ${command}`);
}
