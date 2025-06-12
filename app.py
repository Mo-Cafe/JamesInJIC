from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
from datetime import datetime
import os

app = Flask(__name__)  # ✅ 먼저 선언
CORS(app, origins=["https://jamesinjic.onrender.com"], supports_credentials=True)

@app.route('/api/say', methods=['POST'])
def say():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    filename = f"speech_{int(datetime.now().timestamp())}.mp3"
    filepath = os.path.join("static", filename)

    try:
        tts = gTTS(text, lang='en')
        tts.save(filepath)
        return jsonify({'audio_url': f"/static/{filename}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
