from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging

app = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)

socketio = SocketIO(app, binary=True)
socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def home():
    app.logger.warning('test message 1\ntest message 2\ntest message 3')
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message'

    app.logger.debug('this is a DEBUG message')
    return render_template('index.html')

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    print(request)
    print('Received Chunk of size:', len(chunk))
    print(chunk)

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app, debug=True)