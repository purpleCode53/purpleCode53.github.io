import os
import re
from openai import OpenAI
from datetime import datetime
import pytz

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 시간대 설정 (Asia/Seoul)
tz = pytz.timezone("Asia/Seoul")
now = datetime.now(tz)

# 날짜 설정
today = now.strftime("%Y-%m-%d")
today_datetime = now.strftime("%Y-%m-%d 10:00:00 +0900")

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
   - `tags`: **반드시 `java`, `springboot`, `database`, `ai` 중 하나 이상**을 포함하고, 총 2개 이상 7개 이하의 핵심 키워드
   - `slug`: `title`을 영어로 번역한 후, 소문자로 변환하고 공백과 특수문자는 하이픈(-)으로 치환한 형태로 작성
   - `show_date: false`

2. 주제는 개발자가 실무에서 자주 접하는 문제나 기술 과제를 중심으로 선택해줘.  
   특히 백엔드 개발, 시스템 설계, 성능 최적화, AI 응용, 데이터 처리 등 **현업에서 실질적으로 활용되는 기술**을 다루는 주제면 더욱 좋아.

3. 본문은 블로그 포스팅 스타일로 작성하고, 다음 구성에 맞춰 자연스럽게 이어지는 흐름으로 작성해줘:
   - 서론: 주제에 대한 문제 인식 또는 흥미로운 질문으로 시작
   - 주요 개념 설명
   - 방식 또는 종류별 비교
   - 각 방식의 장단점 분석
   - 마크다운 테이블로 정리
   - 실무에서의 활용 팁
   - 마무리 요약

4. 각 본문 구조의 제목은 "서론", "주요 개념 설명" 같은 고정 문구 대신, **글 내용에 어울리는 자연스러운 소제목**으로 작성해줘.

5. **검색엔진 최적화(SEO)**를 고려해, 해당 주제와 관련된 검색량이 높은 **관련 키워드, 기술용어, 구체적인 표현**을 본문에 적극적으로 사용해줘. 예: "JPA 성능 개선", "Spring Boot 설정 최적화", "AI 모델 튜닝", "데이터베이스 인덱싱 전략" 등

6. 마크다운 문법을 정확히 사용해:
   - 제목은 `##`, 소제목은 `###`, 목록은 `-`, 표는 `|` 사용
   - 코드 블록은 언어명 포함해서 사용 (예: ```java)

7. 문체는 너무 캐주얼하지 않고, **정확하고 실무 중심적인 설명** 위주로 작성해줘.

8. **본문 길이는 1,000자에서 1,200자 사이**로 충분한 기술 정보를 담아줘.

9. GPT가 작성했다는 문구는 절대 포함하지 마.

10. 블로그에 바로 업로드할 수 있는 최종 마크다운 형태로 작성해줘.

※ 핵심: `tags`에는 반드시 `java`, `springboot`, `database`, `ai` 중 하나 이상이 포함되어야 하고, 주제는 실무에 유익한 기술이어야 해.
"""


# GPT API 호출
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

# 결과 마크다운 텍스트
markdown = response.choices[0].message.content

# Front Matter의 slug 필드 추출
slug_match = re.search(r'^slug:\s*(.+)$', markdown, re.MULTILINE)
if slug_match:
    slug = slug_match.group(1).strip()
else:
    # fallback: title 기반 슬러그
    title_match = re.search(r'^title:\s*(?:"|“)?(.+?)(?:"|”)?\s*$', markdown, re.MULTILINE)
    slug = re.sub(r"[^\w\s-]", "", title_match.group(1).strip().lower()) if title_match else "auto"
    slug = re.sub(r"[\s]+", "-", slug)

# 파일 저장
filename = f"_posts/{today}-{slug}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"✅ Blog post saved to: {filename}")
