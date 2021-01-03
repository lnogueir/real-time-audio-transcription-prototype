from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
from flask_pymongo import PyMongo
import os


app = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)
#MONGO DB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)


socketio = SocketIO(app, binary=True)
socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def home():
    app.logger.warning('test message 1\ntest message 2\ntest message 3')
    queryObject  = { "roomID": "testing123"}
    results = mongo.db.Rooms.find(queryObject)
    for result in results:
        print(result["roomID"])
    return render_template('index.html')

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    # print(request)
    # print('Received Chunk of size:', len(chunk))
    app.logger.warning("Recieved audio\n")
    app.logger.warning("lenght of chunk is %d\n", len(chunk))
    print(chunk)

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app, debug=True)