from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)

socketio = SocketIO(app, binary=True)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('begin_transcription')
def handle_begin_transcription():
    print('Began')
    return

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    '''Here put the chunk on the user's session queue'''
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True)