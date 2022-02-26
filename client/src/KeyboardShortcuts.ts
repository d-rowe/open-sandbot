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

function onKeyDown({code}: KeyboardEvent) {
    // prevent conflicts with inputs, text areas, etc
    if (/input|textarea|select/i.test(document.activeElement.nodeName)) {
        return;
    }

    const handler = handlers.get(code);
    if (handler) {
        handler();
    }
}
