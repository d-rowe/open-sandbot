import threading
from flask import Flask, request, Request
from lib import env
from models import track_manager

if not env.is_local:
    from models import bot


def init(app: Flask):
    @app.route('/api/bot/move', methods=['POST'])
    def move():
        # Nothing we can do if we're running locally
        if env.is_local:
            return '', 500

        if bot.in_progress:
            return 'Movement in progress', 409

        operation = request.json['operation']

        if operation == 'MoveToAngles':
            move_to_angles(request)
        elif operation == 'MoveToThetaRho':
            move_to_theta_row(request)
        else:
            return 'Unknown operation', 400

        return '', 201

    @app.route('/api/bot/speed', methods=['POST'])
    def set_speed():
        # Nothing we can do if we're running locally
        if env.is_local:
            return '', 500

        speed = request.json['speed']
        bot.set_speed(speed)

        return '', 201

    @app.route('/api/bot/stop', methods=['POST'])
    def stop():
        # Nothing we can do if we're running locally
        if env.is_local:
            return '', 500

        track_manager.stop()
        bot.stop()

        return '', 201

    @app.route('/api/bot/position', methods=['GET'])
    def get_position():
        # Nothing we can do if we're running locally
        if env.is_local:
            return '', 500

        position = bot.get_position_in_angles()

        return position, 200

    def move_to_angles(req: Request):
        angles = req.json['angles']
        a1 = float(angles[0])
        a2 = float(angles[1])
        threading.Thread(target=bot.to_arm_angles, args=(a1, a2,)).start()

    def move_to_theta_row(req: Request):
        theta = float(req.json['theta'])
        rho = float(req.json['rho'])
        threading.Thread(target=bot.to_theta_rho, args=(theta, rho,)).start()
