import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_captions(news_items):
    results = []
    for item in news_items:
        prompt = create_prompt(item["title"], item["summary"])
        caption = call_gpt(prompt)
        results.append(caption)
        time.sleep(1)
    return results

def create_prompt(title, summary):
    return f"""
너는 스포츠 기자야. 아래 뉴스 제목과 요약을 참고해서 **짧은 기사 형식으로 인스타그램에 올릴 콘텐츠를 작성**해줘.

조건은 다음과 같아:
- 형식: [제목] → [본문] → [해시태그]
- 전체 3~5문장 이내
- 첫 줄은 제목 (뉴스 제목 그대로 쓰되 📣 붙이기)
- 본문은 기사 느낌으로, 간결한 문장 중심
- 마지막 줄에 한글 해시태그 5개 포함

[제목]
{title}

[요약]
{summary}
"""

def call_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # 또는 gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT 호출 실패: {e}"
