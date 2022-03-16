import type {TracksMetadata} from './TrackClient'
import TrackClient from './TrackClient';

export default {
    loadTracksMetada(tracksMetadata: TracksMetadata) {
        const {tracks} = tracksMetadata;
        const fragment = document.createDocumentFragment();

        tracks.forEach(track => {
            const row = document.createElement('tr');
            const nameCell = document.createElement('td');
            const actionCell = document.createElement('td');
            const actionButton = document.createElement('button');
            actionButton.innerText = 'Start';
            actionButton.onclick = () => TrackClient.startTrack(track.track_id);
            actionCell.append(actionButton);

            row.setAttribute('data-track-id', track.track_id);
            nameCell.innerText = track.name;
            row.append(nameCell);
            row.append(actionCell);
            fragment.append(row);
        });

        const body = getTracksTable().querySelector('tbody');
        if (body.children.length) {
            body.innerHTML = '';
        }
        body.append(fragment);
    },

    init,
}

function init() {
    constructHeader();
}

function constructHeader() {
    const tracksTable = getTracksTable();
    const header = document.createElement('thead');
    const body = document.createElement('tbody');
    const headerRow = document.createElement('tr');
    ['Name'].map(cellContent => {
        const cell = document.createElement('th');
        cell.setAttribute('scope', 'col');
        cell.innerText = cellContent;
        headerRow.append(cell);
    });
    header.append(headerRow);
    tracksTable.append(header);
    tracksTable.append(body);
}

function getTracksTable(): HTMLTableElement {
    return document.getElementById('tracks-table') as HTMLTableElement;
}
