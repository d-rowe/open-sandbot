from flask import Flask
from controllers import track_controller,static_content_controller, software_update_controller

app = Flask(__name__, static_folder='../client/dist')


track_controller.init(app)
software_update_controller.init(app)
static_content_controller.init(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
