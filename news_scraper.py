import requests
from bs4 import BeautifulSoup
import re
from utils.sentenceController import truncate_to_full_sentence

def clean_text(text):
    # 공백/광고 제거
    return re.sub(r'\s+', ' ', text).strip()

def get_naver_sports_news(limit=5):
    url = "https://sports.news.naver.com/index"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    news_items = []
    for item in soup.select(".today_item .text"):
        title = item.get_text(strip=True)
        link = item.a['href']
        full_url = "https://sports.news.naver.com" + link
        summary = fetch_naver_article_summary(full_url)
        news_items.append({"title": title, "summary": summary})
        if len(news_items) >= limit:
            break
    return news_items

def fetch_naver_article_summary(article_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.select_one(".news_end") or soup.select_one("#newsEndContents")

        if content:
            text = clean_text(content.get_text())
            return truncate_to_full_sentence(text, max_len=300)
        return "기사 내용을 불러오지 못했습니다."
    except:
        return "요약 실패"

def get_espn_headlines(limit=5):
    base_url = "https://www.espn.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    news_items = []
    for item in soup.select("section[class*='headlineStack'] li a"):
        title = item.get_text(strip=True)
        link = base_url + item['href'] if item['href'].startswith("/") else item['href']
        summary = fetch_espn_article_summary(link)
        news_items.append({"title": title, "summary": summary})
        if len(news_items) >= limit:
            break
    return news_items

def fetch_espn_article_summary(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.select("p")
        text = " ".join([clean_text(p.get_text()) for p in paragraphs if len(p.get_text()) > 50])
        return text[:300] + "..." if len(text) > 300 else text
    except:
        return "기사 내용을 불러오지 못했습니다."

def get_daily_news():
    domestic = get_naver_sports_news(limit=5)
    international = get_espn_headlines(limit=5)
    return domestic + international
