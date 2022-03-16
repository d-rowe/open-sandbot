import os
import track_manager

from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder='../client/dist')


@app.route('/api/tracks-metadata', methods=['GET'])
def get_manifest():
    return track_manager.get_manifest(), 200


@app.route('/api/start-track', methods=['POST'])
def start_track():
    track_id = request.json['trackId']
    track_manager.run(track_id)
    return '', 201


# static assets
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/start', methods=['POST'])
def movement():
    return '', 201


@app.route('/api/software-update', methods=['POST'])
def update():
    stream = os.popen('cd .. && ./update.sh')
    result = stream.read()
    if 'compiled successfully' in result:
        return 'Updated successfully', 201

    return 'Failed to update', 500


if __name__ == '__main__':
    app.run(debug=True)
