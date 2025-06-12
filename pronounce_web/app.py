from flask import Flask, render_template, request, url_for
from gtts import gTTS
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form['text'].strip()
        if text:
            tts = gTTS(text, lang='en')
            filename = f"speech_{int(datetime.now().timestamp())}.mp3"
            filepath = os.path.join("static", filename)
            tts.save(filepath)
            audio_file = filename
    return render_template('index.html', audio_file=audio_file)

if __name__ == '__main__':
    app.run(debug=True)
