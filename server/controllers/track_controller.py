import threading
from models import track_manager
from flask import Flask, request
from lib.endpoint_utils import get_api_endpoint

PATH = 'tracks'


def get_tracks_endpoint(resource: str) -> str:
    return get_api_endpoint(PATH, resource)


def init(app: Flask):
    @app.route(get_tracks_endpoint('metadata'), methods=['GET'])
    def get_manifest():
        return track_manager.get_manifest(), 200

    @app.route(get_tracks_endpoint('start'), methods=['POST'])
    def start_track():
        if track_manager.in_progress:
            return 'Run in progress', 409

        track_id = request.json['trackId']
        track_thread = threading.Thread(target=track_manager.run, args=(track_id,))
        track_thread.start()
        return '', 201

    @app.route(get_tracks_endpoint('import'), methods=['POST'])
    def import_track():
        track_url = request.json['url']
        try:
            track_manager.import_track(track_url)
        except Exception as error:
            # Would be nice to model errors
            return str(error), 500
        return '', 201
