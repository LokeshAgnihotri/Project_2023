// Get the microphone button element
const microphoneButton = document.getElementById('microphone-button');

// Get the text input element
const textBox = document.getElementById('text-box');

// Set up the SpeechRecognition object
const recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;

// Add an event listener to the microphone button
microphoneButton.addEventListener('click', () => {
  // Start listening for speech
  recognition.start();
  
  // Change the button text to "Listening..."
  microphoneButton.textContent = 'Listening...';
});

// Add a result event handler to the recognition object
recognition.onresult = function(event) {
  // Get the recognized text
  const transcript = event.results[0][0].transcript;
  
  // Update the text box with the recognized text
  textBox.value = transcript;
  
  // Change the button text back to "Microphone"
  microphoneButton.textContent = 'Microphone';
};

// Add an error event handler to the recognition object
recognition.onerror = function(event) {
  console.error('Speech recognition error:', event.error);
  
  // Change the button text back to "Microphone"
  microphoneButton.textContent = 'Microphone';
};
