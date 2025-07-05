import requests
from bs4 import BeautifulSoup

def get_naver_sports_news():
    url = "https://sports.news.naver.com/index"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    news_items = []
    for item in soup.select(".today_item .text"):
        title = item.get_text(strip=True)
        link = item.a['href']
        summary = fetch_naver_article_summary("https://sports.news.naver.com" + link)
        news_items.append({"title": title, "summary": summary})
        if len(news_items) >= 3:
            break
    return news_items

def fetch_naver_article_summary(article_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.select_one(".news_end").get_text(strip=True)
        return content[:100] + "..." if content else "기사 내용을 불러오지 못했습니다."
    except:
        return "요약 실패"

def get_espn_headlines():
    url = "https://www.espn.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    news_items = []
    for item in soup.select("section[class*='headlineStack'] li"):
        title = item.get_text(strip=True)
        link = item.a['href'] if item.a else "#"
        news_items.append({
            "title": title,
            "summary": f"해외 스포츠 이슈: {title}",
        })
        if len(news_items) >= 3:
            break
    return news_items

def get_daily_news():
    domestic = get_naver_sports_news()
    international = get_espn_headlines()
    return domestic + international
