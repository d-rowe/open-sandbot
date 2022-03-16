enum LogLevel {
    INFO = 'info',
    ERROR = 'error',
    DEBUG = 'debug',
}

const MAX_LOG_COUNT = 50;

export default {
    info(log: string) {
        addLog(LogLevel.INFO, log);
    },

    error(log: string) {
        addLog(LogLevel.ERROR, log);
    },

    debug(log: string) {
        addLog(LogLevel.DEBUG, log);
    },

    clear() {
        getLogContainer().innerHTML = '';
    },
}

function getLogContainer(): HTMLDivElement {
    return document.getElementById('log-container') as HTMLDivElement;
}

function addLog(level: LogLevel, message: string) {
    const logEntry = document.createElement('p');
    logEntry.innerText = message;
    logEntry.classList.add(`log-${level}`);
    const logContainer = getLogContainer();

    while (logContainer.children.length >= MAX_LOG_COUNT) {
        logContainer.firstChild.remove();
    }

    logContainer.appendChild(logEntry);
    logContainer.scroll({top: logContainer.scrollHeight});
}
