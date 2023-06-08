import json
import os
import webbrowser
import random
import eng_to_ipa as ipa
import pyttsx3
from flask import make_response
import speech_recognition as sr
from pydub import AudioSegment


from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'
rootPath = ''

app.config['UPLOAD_FOLDER'] = 'reference_recordings/'

reference_recordings_path = 'reference_recordings/'
captured_recordings_path = 'captured_recordings/'

@app.route(rootPath+'/')
def main():
    return render_template('UI.html')


@app.route(rootPath+'/reference_recordings/', methods=['GET', 'POST'])
@app.route(rootPath+'/reference_recordings/<file_name>', methods=['GET', 'POST'])
def getAudio(file_name):
    response = make_response(open(reference_recordings_path+file_name, 'rb').read())
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
    return response


@app.route(rootPath+'/receiver', methods=['POST'])
def getAudioFromText():
    event = {'body': json.dumps(request.get_json(force=True))}
    print(event)
    data = request.get_json()
    data = jsonify(data)
    return data

@app.route(rootPath+'/send_text', methods=['POST'])
def getText():
    event = {'body': json.dumps(request.get_json(force=True))}
    print(event)
    data = request.get_json()
    data = jsonify(data)
    return data


@app.route('/random_word')
def random_word():
    with open('english_dictionary.txt', 'r') as file:
        words = file.read().splitlines()
    random_word = random.choice(words)
    random_word_ipa = ipa.convert(random_word)

    # Generate the audio file for the pronunciation
    engine = pyttsx3.init()
    pronunciation_audio_file = f"pronunciation_{random_word}.mpeg"
    engine.save_to_file(random_word, reference_recordings_path + pronunciation_audio_file)
    engine.runAndWait()

    return jsonify({'random_word': random_word, 'random_word_ipa': random_word_ipa,
                    'pronunciation_audio': reference_recordings_path + pronunciation_audio_file})

#https://www.makeuseof.com/tag/python-javascript-communicate-json/



#route to receive the audioop
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        save_path = os.path.join(captured_recordings_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, 'audio.wav')
        audio_file.save(file_path)

        # Convert the recorded audio to text
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)

        # Return the converted text as JSON
        return jsonify({'text': text})
    else:
        return 'No audio file found in the request'

if __name__ == '__main__':
    language = 'en'
    app.run(host="0.0.0.0", port=5000, debug=True)
