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

@app.route('/')
def home():
    app.logger.debug('this is a DEBUG message')
    return render_template('index.html')

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    print(request)
    print('Received Chunk of size:', len(chunk))
    print(chunk)

if __name__ == '__main__':
    socketio.run(app, debug=True)