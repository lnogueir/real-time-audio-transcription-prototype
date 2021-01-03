from flask_socketio import emit, join_room, leave_room
from app import socketio

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    '''Here put the chunk on the user's session queue'''
    pass