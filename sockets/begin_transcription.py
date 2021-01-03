from app import socketio

@socketio.on('begin_transcription')
def handle_begin_transcription():
    print('Began')
    return