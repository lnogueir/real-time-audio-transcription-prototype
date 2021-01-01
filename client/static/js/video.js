const video = document.querySelector('video');

navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream) {
    video.srcObject = stream;
});