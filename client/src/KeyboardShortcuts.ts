type Handler = () => void;

window.addEventListener('keydown', onKeyDown);
const handlers = new Map<string, Handler>();

export default {
    on(key: string, handler: Handler) {
        handlers.set(key, handler);
    },

    off(key: string) {
        handlers.delete(key);
    }
}

function onKeyDown(event: KeyboardEvent) {
    // prevent conflicts with inputs, text areas, etc
    if (/input|textarea|select/i.test(document.activeElement.nodeName)) {
        return;
    }

    const handler = handlers.get(event.code);
    if (handler) {
        event.preventDefault();
        handler();
    }
}
