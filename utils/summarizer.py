"""
Extractive Summarization Module
TF-IDF based summarizer (Railway-safe, no fragile NLTK dependencies)
"""

import heapq
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


# ----------------------------
# STOPWORDS (NO NLTK)
# ----------------------------
STOP_WORDS = set(ENGLISH_STOP_WORDS)


# ----------------------------
# SAFE SENTENCE SPLITTER (NO NLTK)
# ----------------------------
def split_sentences(text: str):
    """
    Lightweight sentence tokenizer using regex.
    Fully stable for deployment.
    """
    return re.split(r'(?<=[.!?])\s+', text.strip())


# ----------------------------
# PREPROCESSING
# ----------------------------
def preprocess_sentence(sentence: str) -> str:
    """
    Clean sentence for TF-IDF scoring.
    """
    words = sentence.lower().split()
    words = [w for w in words if w.isalnum() and w not in STOP_WORDS]
    return " ".join(words)


# ----------------------------
# MAIN SUMMARY FUNCTION
# ----------------------------
def generate_summary(text: str, num_sentences: int = 3) -> str:
    """
    Extractive summarization using TF-IDF sentence scoring.
    """
    if not text or not isinstance(text, str):
        return "No text provided for summarization."

    sentences = split_sentences(text)

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
        return " ".join(sentences[:num_sentences])


# ----------------------------
# FLASK WRAPPER
# ----------------------------
def summarize_email(text: str, num_sentences: int = 3) -> str:
    """
    API wrapper function
    """
    return generate_summary(text, num_sentences)
