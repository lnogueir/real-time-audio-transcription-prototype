from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
from flask_pymongo import PyMongo
import cv2
import base64
import numpy as np
from google.cloud import vision
import os
import io
import time


app = Flask(
    __name__, 
    static_url_path='', 
    static_folder='client/static', 
    template_folder='client/templates'
)
#MONGO DB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

#GOOGLE VISION API
path = 'C:/Users/lukas/Desktop/vision_key.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path
client = vision.ImageAnnotatorClient()

#SOCKET IO
socketio = SocketIO(app, binary=True)
socketio.init_app(app, cors_allowed_origins="*")


#OPEN CV 
haar_cascade=cv2.CascadeClassifier('haar_face.xml')

def bb_hw(bb):
    xmin, ymin, xmax, ymax = bb
    return np.array([xmin, ymin, xmax - xmin + 1, ymax - ymin + 1])

@app.route('/')
def home():
    # app.logger.warning('test message 1\ntest message 2\ntest message 3')
    # queryObject  = { "roomID": "testing123"}
    # results = mongo.db.Rooms.find(queryObject)
    # for result in results:
    #     print(result["roomID"])
    return render_template('index.html')

@socketio.on('begin_transcription')
def handle_begin_transcription():
    print('Began')
    return

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    '''Here put the chunk on the user's session queue'''
    pass

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/api/emotion_handler', methods=['POST'])
def emotion_handler():
    try:
        content = request.get_json(force=True)
    except HTTPException as e:
        return jsonify({'status':0 ,'error': 'Request data invalid'}), 400
    
    start_time = time.time()

    encoded_image = str(content)
    header, data = encoded_image.split(',', 1)

    image_data = base64.b64decode(data)
    #   OPEN CV CODE   #
    # np_array = np.frombuffer(image_data, np.uint8)
    # image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    

    # faces_rect = haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors = 3)
    # rect_list = []

    # for (x,y,w,h) in faces_rect:
    #     # cv2.rectangle(image, (x,y-20), (x+w,y+h+10),(0,255,0),2)
    #     # cv2.imwrite('test.jpeg',image[y-80:y+h+40, x-80:x+w+40])
    #     cropImg = image[y-40:y+h+20, x-40:x+w+20]
    #     rect_list = [x-40,y-40,x+w+20,y+h+20]

    # success, encoded_image = cv2.imencode('.jpeg', image)
    visImg = vision.Image(content=image_data)
    
    response = client.face_detection(image=visImg)
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in response.face_annotations:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {} \n'.format(likelihood_name[face.sorrow_likelihood]))                   

    print("--- %s seconds ---" % (time.time() - start_time))

    # rect_np = bb_hw(rect_list)
    return jsonify({'status':1} )    

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app, debug=True)