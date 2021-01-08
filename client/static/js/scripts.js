const timeslice = 3000;
var socket = io();

var recognition = new webkitSpeechRecognition() || SpeechRecognition();

socket.on('connect', function() {
  console.log('Connected successfully');
});

navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(stream) {

  var mediaRecorder = new RecordRTC(stream, {
    type: 'audio',
    mimeType: 'audio/wav',
    recorderType: StereoAudioRecorder,
    disableLogs: true,
    timeSlice: timeslice,
    ondataavailable: function(blob) {
      // mediaRecorder.stopRecording();
      console.log(blob)
      socket.emit('audio_chunk', blob);
    },
    numberOfAudioChannels: 1,
    desiredSampRate: 16000,
  });
  mediaRecorder.mimeType = 'audio/wav';
  const audioTrack = stream.getAudioTracks()[0];
  audioTrack.applyConstraints({ echoCancellation: true, noiseSuppression: true, channelCount: 1 });
  
  socket.on('ready_to_receive_audio_chunk', () => {
    console.log('Started')
    mediaRecorder.startRecording();
  });

  $('#speaker-button').click(function() {
    var btag = $(this).find('b')
    
    if (btag.html() == 'ON') {
      socket.emit('begin_transcription');

      if (typeof recognition === 'undefined') {
        alert('Browser not supported');
      }

      recognition.continuous = true;
      // recognition.interimResults = true; // Draft transcription enabled
      recognition.lang = 'en';

      recognition.onstart = function() {
        console.log('recognition started');
      };
      
      recognition.onresult = function(event) {
        var transcription = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
          transcription += event.results[i][0].transcript;
        }
        
        console.log(transcription);
      };
      
      recognition.start();
      btag.html('OFF');
    } else {
      mediaRecorder.stopRecording();
      recognition.stop();
      btag.html('ON');
    }
  });

  // mediaRecorder.ondataavailable = function(blob) {
  //   if (mediaRecorder.state !== 'inactive') {
  //     mediaRecorder.stop();
  //     console.log(blob)
  //     socket.emit('audio_chunk', blob);
  //   }
  // }
});




