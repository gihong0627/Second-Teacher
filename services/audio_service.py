import os
import whisper
import tempfile
from pathlib import Path

class AudioService:
    def __init__(self):
        # Whisper 모델 로드 (처음 한 번만 로드)
        self.model = whisper.load_model("tiny")
    
    def transcribe_audio(self, audio_file):
        """오디오 파일을 텍스트로 변환"""
        try:
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                audio_file.save(temp_file.name)
                temp_path = temp_file.name
            
            # Whisper로 음성 인식
            result = self.model.transcribe(temp_path)
            
            # 임시 파일 삭제
            os.unlink(temp_path)
            
            return {
                "success": True,
                "text": result["text"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"오디오 변환 중 오류가 발생했습니다: {str(e)}"
            } 