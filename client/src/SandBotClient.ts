export default {
    async home(): Promise<void> {
        return sendMoveCommand('home');
    },

    async lowerArmLeft() {
        return sendMoveCommand('lower-arm-left');
    },

    async lowerArmRight() {
        return sendMoveCommand('lower-arm-right');
    },

    async upperArmLeft() {
        return sendMoveCommand('upper-arm-left');
    },

    async upperArmRight() {
        return sendMoveCommand('upper-arm-right');
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
        throw new Error('Failed to initiate movement');
    }
}
