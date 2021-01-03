from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
import os
import pymongo



server = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)

#MONGODB setup
server.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(server)
server.config['SESSION_MONGODB'] = mongo.cx


socketio = SocketIO(server, binary=True, manage_session=False)
sess = Session()
server.config['SESSION_TYPE'] = 'mongodb'



from sockets import begin_transcription
from sockets import audio_chunk

from controllers.routes import routes
server.register_blueprint(routes)

# from controllers.api import api
# server.register_blueprint(api)

if __name__ == '__main__':
    server.secret_key = os.environ.get('SESSION_SECRET')
    sess.init_app(server)
    socketio.run(server, debug=True)