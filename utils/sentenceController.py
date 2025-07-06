def truncate_to_full_sentence(text, max_len=300):
    if len(text) <= max_len:
        return text

    sentence_endings = ['.', '?', '!', '。', '！', '？', '…', '．', '․', '。', '·', '‥', 'ㅤ', '⸺', '。', '。', '요.', '다.']
    last_pos = -1
    for punc in sentence_endings:
        pos = text.rfind(punc, 0, max_len)
        if pos > last_pos:
            last_pos = pos + len(punc)

    # 없으면 그냥 자르기
    if last_pos <= 0:
        return text[:max_len] + "..."
    return text[:last_pos]
