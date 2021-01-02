const timeslice = 100;
var socket = io();
socket.on('connect', function() {
  console.log('Connected successfully');
});

navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(stream) {
  var mediaRecorder = new MediaRecorder(stream);
  $('#speaker-button').click(function() {
    var btag = $(this).find('b')
    if (btag.html() == 'ON') {
      socket.emit('begin_transcription', () => {
        mediaRecorder.start(timeslice)
        btag.html('OFF');
      });
    } else {
      mediaRecorder.stop();
      btag.html('ON');
    }
  });

  mediaRecorder.ondataavailable = function(e) {
    socket.emit('audio_chunk', e.data);
  }
});
