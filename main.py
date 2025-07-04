from news_scraper import get_daily_news
from caption_generator import generate_captions
from image_generator import create_image_cards
import os
from datetime import datetime

# 날짜별 폴더 생성
today = datetime.today().strftime("%Y-%m-%d")
output_dir = os.path.join("output", today)
os.makedirs(output_dir, exist_ok=True)

# 1. 뉴스 수집
news_items = get_daily_news()

# 2. 멘트 생성
captions = generate_captions(news_items)

# 3. 이미지 생성 및 저장
create_image_cards(news_items, captions, output_dir)

print(f"총 {len(news_items)}개의 인스타 콘텐츠가 생성되었습니다.")
