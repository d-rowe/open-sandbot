type Handler = () => void;

const handlers = new Map<string, Handler>();

export default {
    init() {
        window.addEventListener('keydown', onKeyDown);
    },

    on(key: string, handler: Handler) {
        handlers.set(key, handler);
    }
}

function onKeyDown(event: KeyboardEvent) {
    const handler = handlers.get(event.code);
    if (handler) {
        handler();
    }
}
