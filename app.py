from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from datetime import datetime
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app, origins=["https://jamesinjic.onrender.com"], supports_credentials=True)

@app.route("/api/say", methods=["POST"])
def say():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"speech_{int(datetime.now().timestamp())}.mp3"
    filepath = os.path.join(app.static_folder, filename)

    try:
        tts = gTTS(text, lang="en")
        tts.save(filepath)
        return jsonify({"audio_url": f"/static/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ index.html 직접 서빙
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# ✅ 기타 잘못된 경로도 index.html로 포워딩 (SPA 대응)
@app.route("/<path:path>")
def catch_all(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
