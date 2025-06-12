from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
from datetime import datetime
import os

# 앱 초기화
app = Flask(__name__)

# CORS 허용 (프론트 도메인만 허용)
CORS(app, origins=["https://jamesinjic.onrender.com"], supports_credentials=True)

# static 폴더 준비
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def root():
    return "TTS API is running."

@app.route('/api/say', methods=['POST'])
def say():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    filename = f"speech_{int(datetime.now().timestamp())}.mp3"
    filepath = os.path.join(STATIC_FOLDER, filename)

    try:
        tts = gTTS(text, lang='en')
        tts.save(filepath)

        return jsonify({
            'audio_url': f"/static/{filename}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
