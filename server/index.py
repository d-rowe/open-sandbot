from flask import Flask
from controllers import static_content_controller
from controllers import movement_controller
from controllers import track_controller
from controllers import software_update_controller

app = Flask(__name__, static_folder='../client/dist')


track_controller.init(app)
movement_controller.init(app)
software_update_controller.init(app)
static_content_controller.init(app)


if __name__ == '__main__':
    app.run(debug=True)
