from flask import Blueprint, request, jsonify
import os
from services.whisper_service import transcribe_audio

stt_bp = Blueprint('stt', __name__)

UPLOAD_FOLDER = 'uploads/'

@stt_bp.route('/api/stt', methods=['POST'])
def stt():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        text = transcribe_audio(file_path)
        return jsonify({"transcription": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
