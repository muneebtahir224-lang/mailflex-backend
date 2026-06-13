import os
import joblib
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")



spam_model = joblib.load(os.path.join(MODEL_DIR, "spam_model.pkl"))
spam_vectorizer = joblib.load(os.path.join(MODEL_DIR, "spam_vectorizer.pkl"))

intent_model = joblib.load(os.path.join(MODEL_DIR, "intent_model.pkl"))
intent_vectorizer = joblib.load(os.path.join(MODEL_DIR, "intent_vectorizer.pkl"))

priority_model = joblib.load(os.path.join(MODEL_DIR, "priority_model.pkl"))
priority_vectorizer = joblib.load(os.path.join(MODEL_DIR, "priority_vectorizer.pkl"))



def clean_email(text):
    return text.lower().strip()



def predict_email(email):

    cleaned = clean_email(email)


    spam_vec = spam_vectorizer.transform([cleaned])
    spam_pred = spam_model.predict(spam_vec)[0]

    if str(spam_pred).lower() == "spam" or spam_pred == 1:
        return {
            "label": "SPAM",
            "intent": None,
            "priority": None
        }


    intent_vec = intent_vectorizer.transform([cleaned])
    intent_pred = intent_model.predict(intent_vec)[0]

    priority_vec = priority_vectorizer.transform([cleaned])
    priority_pred = priority_model.predict(priority_vec)[0]

    return {
        "label": "HAM",
        "intent": intent_pred,
        "priority": priority_pred
    }



from collections import Counter

def predict_long_email(email):

    sentences = re.split(r'(?<=[.!?])\s+', email)

    intents = []
    priorities = []
    spam_count = 0

    for s in sentences:

        cleaned = clean_email(s)

        spam_vec = spam_vectorizer.transform([cleaned])
        spam_pred = spam_model.predict(spam_vec)[0]

        if str(spam_pred).lower() == "spam" or spam_pred == 1:
            spam_count += 1
            continue

        intent_vec = intent_vectorizer.transform([cleaned])
        intent_pred = intent_model.predict(intent_vec)[0]

        priority_vec = priority_vectorizer.transform([cleaned])
        priority_pred = priority_model.predict(priority_vec)[0]

        intents.append(intent_pred)
        priorities.append(priority_pred)

    if spam_count > len(sentences) / 2:
        return {
            "label": "SPAM",
            "intent": None,
            "priority": None
        }

    final_intent = (
        Counter(intents).most_common(1)[0][0]
        if intents else None
    )

    final_priority = (
        Counter(priorities).most_common(1)[0][0]
        if priorities else None
    )

    return {
        "label": "HAM",
        "intent": final_intent,
        "priority": final_priority
    }
