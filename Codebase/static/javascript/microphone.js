var mediaRecorder; // Global variable to store the MediaRecorder instance
var chunks = []; // Array to store recorded audio chunks

function recordfunction() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
      // Permission granted, start recording
      mediaRecorder = new MediaRecorder(stream);

      // Start recording
      mediaRecorder.start();
      alert("Recording has started");

      // Collect the data from the microphone
      mediaRecorder.addEventListener("dataavailable", function(event) {
        chunks.push(event.data);
      });

      // Stop recording after 3 seconds
      setTimeout(function() {
        mediaRecorder.stop();
        alert("Recording has stopped");
        sendAudioData();
      }, 3000);
    })
    .catch(function(error) {
      // Permission denied or error occurred
      // Handle the error or display a message to the user
    });
}

function sendAudioData() {
  // Create a Blob from the recorded audio chunks
  var audioBlob = new Blob(chunks, { type: 'audio/wav' });

  // Create a FormData object
  var formData = new FormData();

  // Append the audio blob
  formData.append('audio', audioBlob, 'audio.wav');

  // Make an HTTP POST request to the Flask backend
  fetch('/upload-audio', {
    method: 'POST',
    body: formData
  })
    .then(function(response) {
      // Handle the response from the backend
      console.log('Audio data sent successfully');
    })
    .catch(function(error) {
      // Handle errors that occurred during the request
      console.error('Error sending audio data:', error);
    });
}


document.getElementById("microphone").addEventListener("click", recordfunction);
