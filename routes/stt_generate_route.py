from flask import Blueprint, request, jsonify
import os
from services.whisper_service import transcribe_audio
from services.question_generator import generate_question
from services.firestore_service import save_question

stt_gen_bp = Blueprint('stt_gen', __name__)
UPLOAD_FOLDER = 'uploads/'

@stt_gen_bp.route('/api/stt-generate', methods=['POST'])
def stt_generate():
    if 'file' not in request.files or 'lecture_id' not in request.form:
        return jsonify({"error": "Missing file or lecture_id"}), 400

    file = request.files['file']
    lecture_id = request.form['lecture_id']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        text = transcribe_audio(file_path)
        question = generate_question(text)
        save_question(lecture_id, question)
        return jsonify({"text": text, "question": question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
