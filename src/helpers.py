from wordcloud import WordCloud, STOPWORDS

def is_valid_message(message) -> bool:
    is_link = 'http' in message.content
    is_mention = '<@' in message.content or "<#" in message.content or message.content.startswith("@")
    is_emoji = '<:' in message.content
    is_empty = message.content == ''
    return not is_link and not is_mention and not is_emoji and not is_empty

def generate_wordcloud(text: str) -> WordCloud:
    return WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = set(STOPWORDS),
                min_font_size = 10).generate(text)