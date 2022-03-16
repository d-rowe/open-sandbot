import threading
from models import track_manager
from flask import Flask, request


def init(app: Flask):
    @app.route('/api/tracks-metadata', methods=['GET'])
    def get_manifest():
        return track_manager.get_manifest(), 200

    @app.route('/api/start-track', methods=['POST'])
    def start_track():
        if track_manager.is_running:
            return 'Run in progress', 409

        track_id = request.json['trackId']
        track_thread = threading.Thread(target=track_manager.run, args=(track_id,))
        track_thread.start()
        return '', 201
