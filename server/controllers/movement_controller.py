import os
import threading
from flask import Flask, request

is_local = bool(os.getenv('LOCAL'))
if not is_local:
    from models import bot


def init(app: Flask):
    @app.route('/api/move-to-angles', methods=['POST'])
    def move_to_angles():
        angles = request.json['angles']
        a1 = float(angles[0])
        a2 = float(angles[1])

        if is_local:
            return '', 500

        track_thread = threading.Thread(target=bot.to_arm_angles, args=(a1, a2,))
        track_thread.start()
        return '', 201
