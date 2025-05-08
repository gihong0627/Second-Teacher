---
Date_of_creation: 2025-05-08 목 23:32:28
Last_modified:
  - 2025-05-08 목 23:40:03
aliases:
  - Second Teacher 백엔드 실행 및 사용법 가이드
tags: 
Reference: 
---
# 1. 📁 프로젝트 실행 준비
---
## 🔧 요구 사항
---
- Python 3.8+
- `ffmpeg` 설치 필요 (Whisper용)
- Firebase 서비스 계정 JSON 키 파일

## 📦 설치 명령어
---
```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. ffmpeg 설치 (Ubuntu 예시)
sudo apt install ffmpeg
```

## 📂 디렉토리 구성
---
```
second-teacher-backend/
├── app.py
├── requirements.txt
├── uploads/
├── routes/
│   ├── stt_route.py
│   └── stt_generate_route.py
├── services/
│   ├── whisper_service.py
│   ├── question_generator.py
│   └── firestore_service.py
└── firebase/
    └── firebase_config.json
```

# 2. ▶️ 서버 실행 방법
---
```bash
python app.py
```

실행 후 접속 주소:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# 3. 🧪 주요 API 사용법
---
## 🔉 1. STT + 문제 생성 + 저장
---
- **POST /api/stt-generate**
- `multipart/form-data`
  - `file`: 음성 파일
  - `lecture_id`: 강의 ID

```bash
curl -X POST http://127.0.0.1:5000/api/stt-generate \
  -F "file=@example.wav" \
  -F "lecture_id=lecture_001"
```

## 🔁 2. STT만 요청
---
- **POST /api/stt**
- `file`: 음성파일
- 텍스트만 반환

# 4. 📦 Firestore 저장 구조
---
```
lectures/
└── lecture_001/
    └── questions/
        └── {자동 생성된 문제 ID}/
            ├── type
            ├── question
            ├── options
            └── answer
```

# 5. ⚠️ 주의 사항
---

| 항목 | 설명 |
|------|------|
| Firebase | `firebase_config.json` 필요 |
| 음성파일 | mp3/wav 형식만 지원 |
| 오류 처리 | 음질 낮으면 빈 결과 반환 가능 |
