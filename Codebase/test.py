import tkinter as tk
import speech_recognition as sr
import nltk
import pyttsx3

# Initialize the NLTK phonetic transcriber
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize the text-to-speech engine with a British English voice
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def convert_audio_to_text():
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)

        # Listen to the user's input
        audio = r.listen(source)

    try:
        # Use Google Speech Recognition to convert audio to text
        text = r.recognize_google(audio)
        text_box.insert(tk.END, "You said: " + text + '\n')
        speak_text(text)

        # Perform phonetic transcription using NLTK
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tagged_words = nltk.pos_tag(words)
            transcribed_words = []
            for tagged_word in tagged_words:
                transcribed_words.append(tagged_word[0] + ' ' + tagged_word[1])
            transcribed_sentence = ' '.join(transcribed_words)
            text_box.insert(tk.END, "Transcription: {}\n".format(transcribed_sentence))

            if sentence.lower() == transcribed_sentence.lower():
                light_canvas.itemconfig(light, fill="green")
            else:
                light_canvas.itemconfig(light, fill="red")
                text_box.insert(tk.END, "You pronounced it incorrectly.\n", "incorrect")
                text_box.insert(tk.END, "Here is the correct pronunciation: {}\n".format(sentence), "incorrect")
                speak_text("You pronounced it incorrectly. Here is the correct pronunciation: {}".format(sentence))

    except sr.UnknownValueError:
        text_box.insert(tk.END, "Sorry, I could not understand what you said.\n", "incorrect")
    except sr.RequestError:
        text_box.insert(tk.END, "Sorry, the service is currently unavailable.\n", "incorrect")

# Create the main window
window = tk.Tk()
window.title("Speech to Text")

# Configure window size and center it on the screen
window.geometry("400x400")
window.eval('tk::PlaceWindow . center')

# Create a frame to hold the text box and button
frame = tk.Frame(window)
frame.pack(pady=10)

# Create the text box
text_box = tk.Text(frame, height=10, width=50)
text_box.pack(side=tk.LEFT, padx=5)

# Create a scroll bar for the text box
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the scroll bar to work with the text box
text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)

# Create the button
button = tk.Button(window, text="Record", command=convert_audio_to_text)
button.pack(pady=5)

# Create a canvas for the light
light_canvas = tk.Canvas(window, width=50, height=50)
light_canvas.pack()

# Create a light shape on the canvas
light = light_canvas.create_oval(10, 10, 40, 40, fill="gray")

# Start

# Start the main event loop
window.mainloop()
