from flask import Flask
from controllers import static_content_controller
from controllers import bot_controller
from controllers import track_controller

app = Flask(__name__, static_folder='../client/build')

CONTROLLERS = [
    track_controller,
    bot_controller,
    static_content_controller,
]

for controller in CONTROLLERS:
    controller.init(app)


if __name__ == '__main__':
    app.run(debug=True)
