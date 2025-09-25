# Autostar

자동으로 스포츠 뉴스를 수집해 인스타그램용 카드 이미지와 캡션을 생성하는 간단한 파이프라인입니다.

## 구성 요소

| 모듈 | 설명 |
| ---- | ---- |
| `news_scraper.py` | 네이버 스포츠와 ESPN에서 최신 기사를 수집하고 요약합니다. |
| `caption_generator.py` | 수집된 기사 내용을 기반으로 LLM을 이용해 인스타그램 스타일의 캡션을 생성합니다. 토큰이 없거나 모델을 불러오지 못하면 간단한 규칙 기반 문구로 대체합니다. |
| `image_generator.py` | 기사 제목과 캡션을 활용한 카드 이미지를 생성하고 텍스트 파일로 캡션을 저장합니다. |
| `main.py` | 전체 파이프라인의 엔트리포인트입니다. |

## 사용 방법

1. Hugging Face API 토큰을 환경 변수 `HUGGINGFACEHUB_API_TOKEN`으로 설정합니다. (선택 사항 – 미설정 시 단순 캡션으로 대체)
2. 필요 패키지를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```

3. 스크립트를 실행합니다.

   ```bash
   python main.py
   ```

4. `output/<날짜>/` 경로에 이미지(`.jpg`)와 캡션(`.txt`)이 저장됩니다.