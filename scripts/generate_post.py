import os
from openai import OpenAI
from datetime import datetime

# posts 디렉토리 생성 (없으면 자동 생성)
os.makedirs("posts", exist_ok=True)

# OpenAI 클라이언트 설정 (환경변수에 API 키 필요)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 오늘 날짜
today = datetime.now().strftime("%Y-%m-%d")

# 블로그 포맷 중심의 프롬프트
prompt = f"""
오늘 날짜는 {today}입니다.

개발자 블로그에 올릴 마크다운 형식의 기술 포스트를 작성해줘. 
주제는 소프트웨어 개발 실무에서 많이 다루는 기술 개념 중 하나를 자유롭게 선택해.

아래 기준을 따라줘:

1. 글은 블로그에 적합한 구조로 구성해줘:
   - 서론 (간결한 도입)
   - 주요 개념 설명
   - 방식 또는 종류별 비교 (2~3개 이상)
   - 각 방식의 장단점 분석
   - 마크다운 테이블로 정리
   - 실무에서의 활용 팁
   - 마무리 요약

2. 마크다운 문법을 정확히 지켜서 작성해줘.
   - ##, ###, -, 표(|), 코드 블록(```java 등) 포함
   - 예시는 실제 실무에 가까운 코드로

3. 문장은 간결하고 정확하게. 설명 중심의 문체로 작성해줘.
   - 너무 캐주얼하지 않고, 정보 전달 중심
   - 최소 600자 이상의 본문 분량으로 작성해줘

4. GPT가 직접 창작한 글이라는 표현은 쓰지 말고, 실제 블로그 포스트처럼 자연스럽게 작성해줘.
"""

# GPT API 호출
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7,
)

# 결과 내용 추출
markdown = response.choices[0].message.content

# 파일 저장
filename = f"_posts/{today}-auto.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"✅ Blog post saved to '{filename}'")
