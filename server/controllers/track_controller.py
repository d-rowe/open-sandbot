import threading
from models import track_manager
from flask import Flask, request


# TODO namespace to /api/tracks/
def init(app: Flask):
    @app.route('/api/tracks-metadata', methods=['GET'])
    def get_manifest():
        return track_manager.get_manifest(), 200

    @app.route('/api/start-track', methods=['POST'])
    def start_track():
        if track_manager.in_progress:
            return 'Run in progress', 409

        track_id = request.json['trackId']
        track_thread = threading.Thread(target=track_manager.run, args=(track_id,))
        track_thread.start()
        return '', 201

    @app.route('/api/import-track', methods=['POST'])
    def import_track():
        track_url = request.json['url']
        try:
            track_manager.import_track(track_url)
        except:
            # Would be nice to model errors
            return 'Invalid track', 400
        return '', 201
