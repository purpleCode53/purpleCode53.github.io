import os
import openai
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

today = datetime.now().strftime("%Y-%m-%d")
prompt = (
    f"오늘 날짜는 {today}입니다. "
    "개발자 블로그용으로, 오늘의 IT/개발 트렌드 3가지를 요약해줘. "
    "제목과 간단한 설명을 포함한 Markdown 형식으로 작성해줘."
)

resp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500,
    temperature=0.7,
)

content = resp.choices[0].message.content.strip()
filepath = f"posts/{today}-auto.md"

with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"---\n")
    f.write(f"title: \"{today} 개발 트렌드 요약\"\n")
    f.write(f"date: {today} 10:00:00 +0900\n")
    f.write(f"categories: [daily, tech]\n")
    f.write(f"tags: [development, trends]\n")
    f.write(f"---\n\n")
    f.write(content)