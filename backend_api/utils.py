import logging
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def calculate_cosine_similarity(text1, text2):
    try:
        vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2), max_features=1000)
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors)[0][1]
        logger.info(f"✅ Similarity calculated: {similarity:.4f}")
        return float(similarity)
    except Exception as e:
        logger.error(f"❌ Error calculating similarity: {str(e)}")
        return 0.0

def highlight_matching_text(text1, text2):
    t1 = text1.lower()
    t2 = text2.lower()
    ngram_matches = set()
    words1 = t1.split()
    words2 = t2.split()
    min_ngram = 4
    max_ngram = 10
    for n in range(min_ngram, max_ngram+1):
        for i in range(len(words1) - n + 1):
            phrase = ' '.join(words1[i:i+n])
            if len(phrase) < 6:
                continue
            if phrase in t2:
                ngram_matches.add(re.escape(phrase))
        for i in range(len(words2) - n + 1):
            phrase = ' '.join(words2[i:i+n])
            if len(phrase) < 6:
                continue
            if phrase in t1:
                ngram_matches.add(re.escape(phrase))
    line_matches = set()
    lines1 = set(line.strip().lower() for line in t1.splitlines() if len(line.strip()) >= 6)
    lines2 = set(line.strip().lower() for line in t2.splitlines() if len(line.strip()) >= 6)
    for line in lines1 & lines2:
        line_matches.add(re.escape(line))
    all_patterns = sorted(ngram_matches | line_matches, key=len, reverse=True)
    h1, h2 = text1, text2
    for pat in all_patterns:
        regex = re.compile(rf'(?i)({pat})')
        h1 = regex.sub(r'<mark>\1</mark>', h1)
        h2 = regex.sub(r'<mark>\1</mark>', h2)
    marks1 = h1.count('<mark>')
    marks2 = h2.count('<mark>')
    if not marks1:
        h1 = f"<p style='background-color: #f0f0f0;'>{text1[:100]}...</p>"
    if not marks2:
        h2 = f"<p style='background-color: #f0f0f0;'>{text2[:100]}...</p>"
    logger.info(f"✅ Robust highlight: {marks1} in text1, {marks2} in text2")
    return h1, h2

def check_plagiarism(text1, text2=''):
    """
    Wrapper to calculate plagiarism similarity.
    If only one text provided, returns 0.0.
    If two texts provided, returns their cosine similarity.
    """
    if text2:
        return calculate_cosine_similarity(text1, text2)
    else:
        # Optionally, implement internet check or return 0
        return 0.0
