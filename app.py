from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import cv2
import base64
import numpy as np

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

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/api/emotion_handler',methods=['POST'])
def emotion_handler():
    try:
        content = request.get_json(force=True)
    except HTTPException as e:
        return jsonify({'error': 'Request data invalid'}), 400
    
    
    encoded_image = str(content)
    header, data = encoded_image.split(',', 1)

    image_data = base64.b64decode(data)
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    return jsonify({'status':0} )    

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    # print(request)
    # print('Received Chunk of size:', len(chunk))
    print(chunk)

if __name__ == '__main__':
    socketio.run(app, debug=True)