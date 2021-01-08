from flask import Flask
from flask_socketio import SocketIO
import os

server = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)

socketio = SocketIO(server, binary=True)


if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="transcription_key.json"
    server.secret_key = 'super secret key'
    server.config['SESSION_TYPE'] = 'filesystem'

    from sockets import transcription_events
    from controllers.api import api
    from controllers.routes import routes
    server.register_blueprint(api)
    server.register_blueprint(routes)

    socketio.run(server, debug=True)