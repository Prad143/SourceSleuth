import praw
from prawcore.exceptions import NotFound
from kafka_producer import KafkaProducer
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, KAFKA_TOPIC_MISC

def scrape_reddit(subreddits):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    kafka_producer = KafkaProducer()

    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
        except NotFound:
            print(f"Error: Subreddit '{subreddit_name}' not found. Skipping...")
            continue
        
        print(f"Processing posts in /r/{subreddit_name}:")
        for submission in subreddit.hot(limit=5):
            if submission.selftext:
                kafka_producer.produce(KAFKA_TOPIC_MISC, {
                    'title': submission.title,
                    'content': submission.selftext
                })

    kafka_producer.flush()