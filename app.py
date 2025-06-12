from flask import Flask, render_template, request, url_for
from gtts import gTTS
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 출처 허용 (개발용)

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
    port = int(os.environ.get("PORT", 10000))  # Render가 자동으로 PORT를 지정해줌
    app.run(host='0.0.0.0', port=port)


