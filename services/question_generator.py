def generate_question(text):
    if "정의" in text:
        return {
            "type": "주관식",
            "question": f"{text.strip()}에 대해 설명하시오.",
        }
    else:
        return {
            "type": "객관식",
            "question": f"{text.strip()}에 대한 설명으로 옳지 않은 것은?",
            "options": [
                f"{text.strip()}은 올바른 개념이다.",
                f"{text.strip()}은 틀린 설명이다.",
                "위의 내용과 무관하다.",
                "모두 올바른 설명이다."
            ],
            "answer": 1
        }
