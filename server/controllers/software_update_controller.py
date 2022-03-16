import os
from flask import Flask


def init(app: Flask):
    @app.route('/api/software-update', methods=['POST'])
    def update():
        stream = os.popen('cd .. && ./update.sh')
        result = stream.read()
        if 'compiled successfully' in result:
            return 'Updated successfully', 201

        return 'Failed to update', 500
