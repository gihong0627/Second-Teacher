# services/gemini_service.py
import os
import requests
import json
import PyPDF2
import io
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class GeminiService:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
    
    def summarize_pdf(self, pdf_file, prompt_option=1):
        """PDF 파일을 분석하여 요약"""
        try:
            # PDF 파일에서 텍스트 추출
            pdf_text = self._extract_text_from_pdf(pdf_file)
            
            if not pdf_text.strip():
                return {
                    "success": False,
                    "error": "PDF에서 텍스트를 추출할 수 없습니다."
                }
            
            # 텍스트가 너무 길면 잘라내기 (Gemini 토큰 제한)
            if len(pdf_text) > 30000:
                pdf_text = pdf_text[:30000] + "... (텍스트가 너무 길어 일부 생략되었습니다)"
            
            # 선택한 옵션에 따라 프롬프트 설정
            prompt = self._get_prompt_by_option(prompt_option, pdf_text)
            
            # Gemini에 요약 요청
            return self._send_gemini_request(prompt)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"PDF 요약 처리 중 오류가 발생했습니다: {str(e)}"
            }
    
    def _extract_text_from_pdf(self, pdf_file):
        """PDF 파일에서 텍스트 추출"""
        # 파일 위치 저장
        current_position = pdf_file.tell()
        # 파일 포인터를 처음으로 이동
        pdf_file.seek(0)
        
        file_content = pdf_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        
        text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        
        # 파일 포인터 원래 위치로 복원
        pdf_file.seek(current_position)
        return text
    
    def _get_prompt_by_option(self, option, pdf_text):
        """옵션에 따른 프롬프트 반환"""
        prompts = {
            1: f"다음 PDF 문서의 내용을 한국어로 간결하게 요약해주세요. 주요 내용과 핵심 포인트에 초점을 맞춰주세요.\n\n{pdf_text}",
            2: f"다음 PDF 문서의 내용을 한국어로 상세하게 요약해주세요. 주요 내용과 핵심 포인트를 모두 포함하되, 각 섹션별로 구분하여 요약해주세요. 정보의 손실을 최소화하면서 원본 내용의 구조를 유지해주세요.\n\n{pdf_text}"
        }
        
        return prompts.get(option, prompts[1])  # 기본값은 옵션 1
    
    def _send_gemini_request(self, prompt):
        """Gemini API에 요청 보내기"""
        try:
            request_data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                data=json.dumps(request_data),
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    content = result["candidates"][0]["content"]
                    parts = content.get("parts", [])
                    if parts and "text" in parts[0]:
                        return {
                            "success": True,
                            "summary": parts[0]["text"]
                        }
            
            return {
                "success": False,
                "error": f"API 요청 실패: {response.status_code}, {response.text}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }