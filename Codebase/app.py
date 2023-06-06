from flask import Flask, render_template, jsonify
import random
import eng_to_ipa as ipa
import pyttsx3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_word')
def random_word():
    with open('C:/Users/lokes/OneDrive/Desktop/project_2023/Project_2023/Codebase/english_dictionary.txt', 'r') as file:
        words = file.read().splitlines()
    random_word = random.choice(words)
    random_word_ipa = ipa.convert(random_word)
    
    # Generate the audio file for the pronunciation
    engine = pyttsx3.init()
    pronunciation_audio_file = f"pronunciation_{random_word}.wav"
    engine.save_to_file(random_word, pronunciation_audio_file)
    engine.runAndWait()
    
    return jsonify({'random_word': random_word, 'random_word_ipa': random_word_ipa, 'pronunciation_audio': pronunciation_audio_file})

if __name__ == '__main__':
    app.run()
