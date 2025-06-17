import os
import openai
from datetime import datetime
import re

# 🔑 환경 변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📅 오늘 날짜 및 시간
today = datetime.now().strftime("%Y-%m-%d")
formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")

# 🧠 GPT 프롬프트 설정
prompt = (
    f"오늘 날짜는 {today}입니다. "
    "개발자 블로그용 포스트를 작성해줘. 주제는 '오늘의 IT/개발 트렌드 3가지'이고, "
    "각 트렌드에 대해 간단한 제목과 요약을 포함한 Markdown 포맷으로 작성해줘. "
    "그리고 전체 내용을 요약한 한 문장짜리 excerpt도 생성해줘."
)

# 💬 GPT API 호출
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # 필요 시 gpt-4-turbo로 변경 가능
    messages=[{"role": "user", "content": prompt}],
    max_tokens=700,
    temperature=0.7,
)

# 📄 GPT 응답 내용
content = response.choices[0].message.content.strip()

# 📝 excerpt 자동 추출
excerpt_match = re.search(r'(Excerpt|요약)[^\n]*:\s*(.+)', content, re.IGNORECASE)
excerpt = excerpt_match.group(2).strip() if excerpt_match else "GPT가 자동 생성한 개발 트렌드 요약입니다."

# 📂 파일 경로 설정
filepath = f"posts/{today}-auto.md"

# 🧾 Markdown 파일로 저장
with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"---\n")
    f.write(f"title: \"{today} 개발 트렌드 요약\"\n")
    f.write(f"excerpt: \"{excerpt}\"\n")
    f.write(f"date: {formatted_time}\n")
    f.write(f"categories: [daily, tech]\n")
    f.write(f"tags: [development, trends]\n")
    f.write(f"author: purplecode53\n")
    f.write(f"robots: index, follow\n")
    f.write(f"canonical_url: https://purplecode53.github.io/posts/{today}-auto/\n")
    f.write(f"layout: single\n")
    f.write(f"---\n\n")
    f.write(content)
