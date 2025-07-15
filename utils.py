import re
from datetime import datetime, timedelta

def is_recent(post_date, days_back):
    return post_date >= datetime.now() - timedelta(days=days_back)

def contains_free_terms(text):
    terms = ["free", "open-source", "no cost", "new", "launch", "released", "introducing", "just launched", "now available"]
    return any(term in text.lower() for term in terms)

def extract_links(text):
    return re.findall(r'(https?://\S+)', text)
