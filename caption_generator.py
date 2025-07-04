def generate_captions(news_items):
    # 실제 구현에서는 LLM이나 RAG로 멘트 생성
    results = []
    for item in news_items:
        text = item["title"]
        summary = item["summary"]
        caption = f"📣 {text}\n{summary}\n\n#스포츠뉴스 #오늘의이슈 #하이라이트"
        results.append(caption)
    return results
