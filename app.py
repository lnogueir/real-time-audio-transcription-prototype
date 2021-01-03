from flask import Flask
from flask_socketio import SocketIO

server = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)

socketio = SocketIO(server, binary=True)

from sockets import begin_transcription
from sockets import audio_chunk

from controllers.routes import routes
server.register_blueprint(routes)

from controllers.api import api
server.register_blueprint(api)

if __name__ == '__main__':
    socketio.run(server, debug=True)