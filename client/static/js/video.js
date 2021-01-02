const API_URL = '/api/emotion_handler'
const video = document.querySelector('video');
const canvas = document.querySelector("#video-container > canvas");
var currStream, imageCapture;

const test = {
    'name':'Lukas',
    'date':'11/12/2000'
};

$('#video-button').click(function() {
    var btag = $(this).find('b')

    if (btag.html() == 'ON') {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
            currStream = stream;
        });
      btag.html('OFF');
    } else {
        video.srcObject = null;
        currStream.getTracks().forEach(function(track){
        if (track.readyState == 'live' && track.kind === 'video') {
            track.stop();
            }
        });
        currStream = null;
        btag.html('ON');
    }
  });

function sendFrame(imageUrl){
    fetch(API_URL,{
        method: 'POST',
        body: JSON.stringify(imageUrl),
        headers: {
            'content-type': 'application/json'
        }
        }).then(resp => resp.json()
            .then(data => console.log(data)))
}


function capture() {
    var canvas = document.querySelector('canvas');     
    var video = document.querySelector('video');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);  
    
    imageCapture = canvas.toDataURL("image/jpeg");

    image.src = imageCapture;
    sendFrame(imageCapture);
}