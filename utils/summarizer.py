"""
Extractive Summarization Module
Uses TF-IDF sentence scoring to generate summaries.
"""

import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


setup_nltk()
STOP_WORDS = set(stopwords.words("english"))



def preprocess_sentence(sentence: str) -> str:
    """
    Clean and preprocess a sentence for TF-IDF scoring.
    """
    words = word_tokenize(sentence.lower())
    words = [w for w in words if w.isalnum() and w not in STOP_WORDS]
    return " ".join(words)



def generate_summary(text: str, num_sentences: int = 3) -> str:
    """
    Generate extractive summary using TF-IDF sentence scoring.
    """
    if not text or not isinstance(text, str):
        return "No text provided for summarization."

    sentences = sent_tokenize(text)

    
    if len(sentences) <= num_sentences:
        return text

    
    processed = [preprocess_sentence(s) for s in sentences]

    
    valid_data = [
        (i, sent, proc)
        for i, (sent, proc) in enumerate(zip(sentences, processed))
        if proc.strip()
    ]

    if not valid_data:
        return text[:500] + "..." if len(text) > 500 else text

    indices, original_sentences, processed_sentences = zip(*valid_data)

    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_sentences)

        sentence_scores = {
            idx: tfidf_matrix[i].sum()
            for i, idx in enumerate(indices)
        }

        
        top_indices = heapq.nlargest(
            min(num_sentences, len(sentence_scores)),
            sentence_scores,
            key=sentence_scores.get
        )

    
        ordered = [sentences[i] for i in sorted(top_indices)]

        return " ".join(ordered)

    except Exception:
        # Safe fallback
        return " ".join(sentences[:num_sentences])


def get_word_count(text: str) -> int:
    """
    Returns word count of a text.
    """
    if not text:
        return 0
    return len(text.split())


def summarize_email(text: str, num_sentences: int = 3) -> str:
    """
    Simple wrapper for Flask API usage.
    """
    return generate_summary(text, num_sentences)
