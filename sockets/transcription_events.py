import keras
import numpy as np
from flask import request, session
from flask_socketio import emit, join_room, leave_room
from six.moves import queue
from audioset import vggish_embeddings
from __main__ import socketio

model = keras.models.load_model('Models/LSTM_SingleLayer_100Epochs.h5')
audio_embed = vggish_embeddings.VGGishEmbedder()

def chunk_generator(user_sess):
  while not(user_sess['transcription_done']):
    # Use a blocking get() to ensure there's at least one chunk of
    # data, and stop iteration if the chunk is None, indicating the
    # end of the audio stream.
    chunk = user_sess['transcription_queue'].get()
    if chunk is None:
        return
    data = [chunk]

    # Now consume whatever other data's still buffered.
    while True:
        try:
            chunk = user_sess['transcription_queue'].get(block=False)
            if chunk is None:
                return
            data.append(chunk)
        except queue.Empty:
            break
    yield b"".join(data)

@socketio.on('begin_transcription')
def handle_begin_transcription():
  session['transcription_done'] = False
  session['transcription_queue'] = queue.Queue()

  emit('ready_to_receive_audio_chunk', room=request.sid)

  audio_generator = chunk_generator(session)
  
  for chunk in audio_generator:
    print('Got Chunk')
    arr = np.frombuffer(chunk, dtype=np.int16)
    print('LEN IS:', len(arr))
    embeddings = audio_embed.convert_waveform_to_embedding(arr, 16000)
    p = model.predict(np.expand_dims(embeddings, axis=0))    
    laugh_score = p[0, 0]
    print('Laugh Score: {0:0.6f}'.format(laugh_score))
    print('Most likely laughing' if laugh_score >= 0.6 else 'Probably not laughing')
  return 

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
  audio_chunk = np.frombuffer(chunk, dtype=np.int16)
  session['transcription_queue'].put(audio_chunk)

@socketio.on('end_transcription')
def handle_end_transcription():
  user_sess['transcription_done'] = True
  session['transcription_queue'].put(None)
