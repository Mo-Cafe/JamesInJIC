from flask import Flask, render_template, request
from gtts import gTTS
from datetime import datetime
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://jamesinjic.onrender.com"], supports_credentials=True)

STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            filename = f"speech_{int(datetime.now().timestamp())}.mp3"
            filepath = os.path.join(STATIC_FOLDER, filename)

            tts = gTTS(text, lang='en')
            tts.save(filepath)
            audio_file = filename

    return render_template('index.html', audio_file=audio_file)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
