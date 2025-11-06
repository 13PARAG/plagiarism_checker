"""
Google Custom Search Integration Module
File: backend_api/google_search_integration.py

Handles internet-wide plagiarism detection using Google Custom Search API
"""
from dotenv import load_dotenv; load_dotenv()
import os
import requests
import logging
from typing import List, Dict
import time
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")

# Constants
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
MAX_RESULTS_PER_QUERY = 5
NUM_KEY_SENTENCES = 3


def extract_key_sentences(text: str, num_sentences: int = NUM_KEY_SENTENCES) -> List[str]:
    """
    Extract important sentences from text for searching.
    Args:
        text (str): Input text to extract from
        num_sentences (int): Number of sentences to extract
    Returns:
        list: List of key sentences
    """
    try:
        # Split by sentence
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        meaningful = [s for s in sentences if len(s) > 30]
        meaningful.sort(key=len, reverse=True)
        selected = meaningful[:num_sentences]
        logger.info(f"✓ Extracted {len(selected)} key sentences from text")
        return selected
    except Exception as e:
        logger.error(f"Error extracting sentences: {str(e)}")
        return []


def search_google_cse(query: str, num_results: int = MAX_RESULTS_PER_QUERY) -> List[Dict]:
    """
    Search using Google Custom Search Engine API.
    Args:
        query (str): Search query
        num_results (int): Number of results to return
    Returns:
        list: List of search results with title, link, snippet
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        logger.error("❌ Google API credentials not configured")
        return []
    try:
        params = {
            'q': query,
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'num': num_results,
            'start': 1
        }
        logger.info(f"🔍 Searching Google CSE for: {query[:50]}...")
        response = requests.get(GOOGLE_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        results_data = response.json()
        if 'items' in results_data:
            results = []
            for item in results_data['items'][:num_results]:
                results.append({
                    'title': item.get('title', 'Untitled'),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
            logger.info(f"✓ Found {len(results)} results")
            return results
        else:
            logger.warning(f"⚠️ No results found for: {query}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching Google CSE: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in Google search: {str(e)}")
        return []


def compare_with_internet_sources(submission_text: str) -> Dict:
    """
    Compare submission against internet sources.
    Args:
        submission_text (str): Text to check for plagiarism
    Returns:
        dict: Results with top matches, URLs, and similarity scores
    """
    from utils import calculate_cosine_similarity, highlight_matching_text
    import joblib

    logger.info("=" * 60)
    logger.info("🌐 STARTING INTERNET PLAGIARISM CHECK")
    logger.info("=" * 60)

    try:
        model_path = "plagiarism_model.pkl"
        if not os.path.exists(model_path):
            logger.error(f"❌ Model file not found: {model_path}")
            return {
                "status": "error",
                "message": "ML model not found. Please train the model first."
            }
        model = joblib.load(model_path)
        logger.info("✓ Model loaded successfully")

        key_sentences = extract_key_sentences(submission_text, num_sentences=NUM_KEY_SENTENCES)
        if not key_sentences:
            logger.warning("⚠️ Could not extract key sentences")
            return {
                "status": "error",
                "message": "Could not extract key sentences from submission"
            }
        logger.info(f"📝 Key sentences to search: {len(key_sentences)}")

        all_matches = {}
        processed_urls = set()

        for idx, sentence in enumerate(key_sentences, 1):
            logger.info(f"\n[Query {idx}/{len(key_sentences)}] Searching: {sentence[:60]}...")
            results = search_google_cse(sentence, num_results=MAX_RESULTS_PER_QUERY)
            time.sleep(0.5)
            for result in results:
                url = result['link']
                if url in processed_urls:
                    logger.info(f"  ⊘ Skipping duplicate URL: {url}")
                    continue
                processed_urls.add(url)
                snippet = result['snippet']
                title = result['title']
                logger.info(f"  → Processing: {title[:50]}...")
                try:
                    similarity = calculate_cosine_similarity(snippet, submission_text)
                    prediction = int(model.predict([[similarity]])[0])
                    probability = float(model.predict_proba([[similarity]])[0][1])
                    highlighted_snippet, highlighted_sub = highlight_matching_text(
                        snippet, submission_text
                    )
                    if url not in all_matches or similarity > all_matches[url]['similarity_score']:
                        all_matches[url] = {
                            'url': url,
                            'title': title,
                            'snippet': snippet,
                            'similarity_score': round(similarity, 4),
                            'plagiarized': bool(prediction),
                            'probability': round(probability, 4),
                            'highlighted_snippet': highlighted_snippet,
                            'highlighted_submission': highlighted_sub
                        }
                    logger.info(f"    ✓ Similarity: {similarity:.4f} | Plagiarized: {bool(prediction)}")
                except Exception as e:
                    logger.error(f"    ✗ Error processing result: {str(e)}")
                    continue

        matches_list = list(all_matches.values())
        matches_list.sort(key=lambda x: x['similarity_score'], reverse=True)
        top_matches = matches_list[:5]
        verdict = "PLAGIARIZED" if (top_matches and top_matches[0]['plagiarized']) else "LIKELY ORIGINAL"

        # === FIX: Return correct info for Telegram and API ===
        if top_matches:
            best = top_matches[0]
            result = {
                "status": "success",
                "similarity_score": int(best['similarity_score'] * 100),   # Percentage integer
                "top_match_title": best['title'],
                "top_match_url": best['url'],
                "overall_verdict": verdict,
                "internet_matches": top_matches,
                "total_matches_found": len(top_matches),
                "highest_similarity": best['similarity_score']
            }
        else:
            result = {
                "status": "success",
                "similarity_score": 0,
                "top_match_title": "",
                "top_match_url": "",
                "overall_verdict": verdict,
                "internet_matches": [],
                "total_matches_found": 0,
                "highest_similarity": 0.0,
            }

        logger.info("\n" + "=" * 60)
        logger.info("✅ INTERNET PLAGIARISM CHECK COMPLETE")
        logger.info(f"   Total matches: {len(top_matches)}")
        logger.info(f"   Highest similarity: {result['highest_similarity']:.4f}")
        logger.info(f"   Verdict: {verdict}")
        logger.info("=" * 60)

        return result

    except Exception as e:
        logger.error(f"❌ Error in internet plagiarism check: {str(e)}")
        return {
            "status": "error",
            "message": f"Error checking plagiarism: {str(e)}"
        }


def validate_credentials() -> bool:
    """
    Validate Google API credentials.
    Returns:
        bool: True if credentials are valid
    """
    if not GOOGLE_API_KEY:
        logger.error("❌ GOOGLE_API_KEY not set")
        return False
    if not GOOGLE_CSE_ID:
        logger.error("❌ GOOGLE_CSE_ID not set")
        return False
    logger.info("✓ Google API credentials configured")
    return True
