import os
from bot import tracks
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../client/dist')


# static assets
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    tracks.run('zelda_triangles')
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
    app.run(debug=True, use_reloader=True, port=5000, host="0.0.0.0")
