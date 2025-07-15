import tweepy
from datetime import datetime, timedelta
from config import KEYWORDS, DAYS_BACK
from utils import contains_free_terms, extract_links
import os
from dotenv import load_dotenv

load_dotenv()

def get_twitter_client():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        raise ValueError("TWITTER_BEARER_TOKEN not set in .env file")
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

def scrape_x():
    client = get_twitter_client()
    results = []
    since_date = (datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%dT%H:%M:%SZ')

    for keyword in KEYWORDS:
        query = f'{keyword} -is:retweet lang:en'
        for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=['created_at', 'author_id', 'text'],
            start_time=since_date,
            max_results=50
        ).flatten(limit=200):
            text = tweet.text
            post_date = tweet.created_at
            if contains_free_terms(text):
                results.append({
                    "platform": "X",
                    "keyword": keyword,
                    "text": text,
                    "date": post_date,
                    "author": tweet.author_id,
                    "links": extract_links(text)
                })
    return results
