import os
import re
import unicodedata
from openai import OpenAI
from datetime import datetime

# OpenAI 클라이언트 초기화 (환경변수에서 API 키 가져옴)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 오늘 날짜
today = datetime.now().strftime("%Y-%m-%d")
today_datetime = datetime.now().strftime("%Y-%m-%d 10:00:00 +0900")

# slugify 함수 (파일명용)
def slugify(text):
    text = re.sub(r"[^\w\s가-힣-]", "", text)
    text = text.strip().lower()
    return re.sub(r"[\s]+", "-", text)

# 디렉토리 생성
os.makedirs("_posts", exist_ok=True)

# GPT에게 보낼 프롬프트
prompt = f"""
오늘 날짜는 {today}입니다.

개발자 블로그에 올릴 기술 포스트를 작성해줘.  
아래 기준을 반드시 지켜줘:

1. 글 상단에 Jekyll 블로그용 **Front Matter**를 YAML 형식으로 포함해줘. `---`로 감싸고 다음 항목을 채워줘:
   - `layout: single`
   - `title`: 글의 주제를 명확하게 표현
   - `date`: 오늘 날짜와 시간 (형식: YYYY-MM-DD HH:mm:ss +0900)
   - `categories`: 글의 주제에 맞는 1개 이상의 카테고리
   - `tags`: 관련된 핵심 키워드 **3개에서 7개 사이**
   - `show_date: false`

2. 본문은 다음 구조를 따라줘:
   - 서론 (문제 인식 또는 주제 도입)
   - 주요 개념 설명
   - 방식 또는 종류별 비교 (2~3개 이상)
   - 각 방식의 장단점 분석
   - 마크다운 테이블로 정리
   - 실무에서의 활용 팁
   - 마무리 요약

3. 마크다운 문법을 정확히 사용해:
   - 제목은 `##`, 소제목은 `###`, 목록은 `-`, 표는 `|` 사용
   - 코드 블록은 언어명 포함해서 사용 (예: ```java)

4. 문체는 너무 캐주얼하지 않고, **정확하고 실무적인 설명** 위주로 작성해줘.

5. **최소 800자**, 가능하면 **1,000자에 가까운 본문 분량**으로 충분한 내용을 담아줘.

6. GPT가 작성했다는 문구는 절대 포함하지 마.

7. 블로그에 바로 업로드할 수 있는 최종 마크다운 형태로 작성해줘.

※ 위 기준을 철저히 따라줘.
"""

# GPT API 호출
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

# 결과 마크다운 텍스트
markdown = response.choices[0].message.content

# 제목에서 슬러그 추출 (title: "..." 라인 찾기)
match = re.search(r'^title:\s*["“](.+?)["”]', markdown, re.MULTILINE)
if match:
    raw_title = match.group(1)
    slug = slugify(raw_title)
else:
    slug = "auto"

# 파일 저장
filename = f"_posts/{today}-{slug}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"✅ Blog post saved to: {filename}")
