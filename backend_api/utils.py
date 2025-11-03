# """
# Utility functions for plagiarism detection
# Module: plagiarism_checker/backend_api/utils.py

# This module contains core utility functions for:
# - Text similarity calculation using TF-IDF and cosine similarity
# - Text highlighting to identify matching segments
# - Binary classification support
# """

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import difflib
# import numpy as np


# def preprocess_text(text):
#     """
#     Preprocess text by cleaning and normalizing
    
#     Args:
#         text (str): Raw text to preprocess
    
#     Returns:
#         str: Cleaned text
#     """
#     # Remove extra whitespace and normalize
#     text = ' '.join(text.split())
#     return text.lower()


# def calculate_cosine_similarity(text1, text2):
#     """
#     Calculate cosine similarity between two texts using TF-IDF vectorization
    
#     This function converts texts to TF-IDF vectors and computes cosine similarity.
#     TF-IDF (Term Frequency-Inverse Document Frequency) gives higher weights to 
#     unique terms while minimizing common words.
    
#     Args:
#         text1 (str): First text document (original)
#         text2 (str): Second text document (submission)
    
#     Returns:
#         float: Cosine similarity score ranging from 0 to 1
#                 - 0: completely different texts
#                 - 1: identical texts
    
#     Raises:
#         ValueError: If either text is empty
    
#     Examples:
#         >>> score = calculate_cosine_similarity("hello world", "hello world")
#         >>> assert score == 1.0
#         >>> score = calculate_cosine_similarity("cats", "dogs")
#         >>> assert 0 <= score <= 1
#     """
#     # Validate inputs
#     if not text1.strip() or not text2.strip():
#         raise ValueError("Text inputs cannot be empty")
    
#     try:
#         # Create TF-IDF vectorizer
#         # max_features: limit to most important features
#         # ngram_range: consider both unigrams and bigrams
#         vectorizer = TfidfVectorizer(
#             max_features=1000,
#             ngram_range=(1, 2),
#             lowercase=True,
#             stop_words='english'
#         )
        
#         # Fit and transform both texts
#         tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
#         # Calculate cosine similarity
#         similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
#         # Extract and return the similarity score
#         similarity_score = float(similarity_matrix[0][0])
        
#         return similarity_score
    
#     except Exception as e:
#         raise ValueError(f"Error calculating similarity: {str(e)}")


# def label_similarity(similarity_score, threshold=0.8):
#     """
#     Convert similarity score to binary label for classification
    
#     Args:
#         similarity_score (float): Similarity score (0-1)
#         threshold (float): Classification threshold (default: 0.8)
#                           Scores >= threshold classified as plagiarized (1)
#                           Scores < threshold classified as original (0)
    
#     Returns:
#         int: 1 for plagiarized, 0 for original
    
#     Raises:
#         ValueError: If similarity_score is not between 0 and 1
#     """
#     if not (0 <= similarity_score <= 1):
#         raise ValueError(f"Similarity score must be between 0 and 1, got {similarity_score}")
    
#     return int(similarity_score >= threshold)


# def highlight_matching_text(text1, text2, min_match_length=3):
#     """
#     Highlight matching segments between two texts using HTML <mark> tags
    
#     Uses difflib.SequenceMatcher to identify contiguous matching sequences
#     and wraps them with HTML <mark> tags for visual highlighting.
    
#     Args:
#         text1 (str): Original text document
#         text2 (str): Submission text document
#         min_match_length (int): Minimum length of matching sequence to highlight
    
#     Returns:
#         tuple: (highlighted_text1, highlighted_text2)
#             - Both are HTML-formatted strings with <mark> tags around matches
    
#     Raises:
#         ValueError: If either text is empty
    
#     Examples:
#         >>> orig = "The quick brown fox"
#         >>> subm = "The quick brown dog"
#         >>> h1, h2 = highlight_matching_text(orig, subm)
#         >>> "<mark>" in h1 and "<mark>" in h2
#         True
#     """
#     if not text1.strip() or not text2.strip():
#         raise ValueError("Text inputs cannot be empty")
    
#     try:
#         # Create sequence matcher
#         matcher = difflib.SequenceMatcher(
#             isjunk=lambda x: x in ' \t\n',  # Ignore whitespace
#             a=text1,
#             b=text2
#         )
        
#         # Get matching blocks
#         blocks = matcher.get_matching_blocks()
        
#         def wrap_highlight(text, blocks, is_text1=True, min_len=min_match_length):
#             """Helper function to wrap matching segments with HTML marks"""
#             result = []
#             last_idx = 0
            
#             for block in blocks:
#                 # Get start position based on which text
#                 start = block.a if is_text1 else block.b
#                 length = block.size
                
#                 # Only highlight if match length is significant
#                 if length < min_len:
#                     continue
                
#                 # Add non-matching text
#                 if start > last_idx:
#                     result.append(text[last_idx:start])
                
#                 # Add matching text with highlight tag
#                 matching_text = text[start:start + length]
#                 # Escape HTML special characters
#                 matching_text = (matching_text
#                                 .replace('&', '&amp;')
#                                 .replace('<', '&lt;')
#                                 .replace('>', '&gt;'))
#                 result.append(f"<mark>{matching_text}</mark>")
                
#                 last_idx = start + length
            
#             # Add remaining text
#             remaining = text[last_idx:]
#             remaining = (remaining
#                         .replace('&', '&amp;')
#                         .replace('<', '&lt;')
#                         .replace('>', '&gt;'))
#             result.append(remaining)
            
#             return ''.join(result)
        
#         # Highlight both texts
#         highlighted1 = wrap_highlight(text1, blocks, is_text1=True)
#         highlighted2 = wrap_highlight(text2, blocks, is_text1=False)
        
#         return highlighted1, highlighted2
    
#     except Exception as e:
#         raise ValueError(f"Error highlighting text: {str(e)}")


# def calculate_word_overlap(text1, text2):
#     """
#     Calculate word-level overlap between two texts
    
#     Args:
#         text1 (str): First text
#         text2 (str): Second text
    
#     Returns:
#         dict: Statistics including overlap percentage and unique words
#     """
#     words1 = set(text1.lower().split())
#     words2 = set(text2.lower().split())
    
#     overlap = words1.intersection(words2)
#     union = words1.union(words2)
    
#     overlap_ratio = len(overlap) / len(union) if union else 0
    
#     return {
#         'overlap_count': len(overlap),
#         'overlap_ratio': overlap_ratio,
#         'text1_unique': len(words1 - words2),
#         'text2_unique': len(words2 - words1),
#         'common_words': list(overlap)[:10]  # First 10 common words
#     }














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
