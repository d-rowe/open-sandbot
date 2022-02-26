enum LogLevel {
    INFO = 'info',
    ERROR = 'error',
    DEBUG = 'debug',
}

const MAX_LOG_COUNT = 200;
let logCount = 0;

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
    return document.querySelector('.log-container');
}

function addLog(level: LogLevel, message: string) {
    const logEntry = document.createElement('p');
    logEntry.innerText = message;
    logEntry.classList.add(`log-${level}`);
    const logContainer = getLogContainer();

    while (logCount >= MAX_LOG_COUNT - 1) {
        logContainer.firstChild.remove();
        logCount -= 1;
    }

    logContainer.appendChild(logEntry);
    logCount += 1;
    logContainer.scroll({top: logContainer.scrollHeight});
}
