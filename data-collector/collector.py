import os
import re
import uuid
import json
import pika
from datetime import datetime
import tweepy
from dotenv import load_dotenv

from db import session, Base, engine, get_last_job_end_date
from models.job import Job


def init():
    load_dotenv()
    bearer_token = os.getenv('BEARER_TOKEN')

    if not bearer_token:
        raise ValueError("Bearer token not found. Please set it in the .env file.")
    return bearer_token

def get_tweets(max_results, bearer_token, start_time=None):
    client = tweepy.Client(bearer_token=bearer_token)

    query = (
        '("Artificial Intelligence" OR "#ai" OR "#artificialintelligence" OR "Machine Learning" OR "AI ethics" '
        'OR "AI bias" OR "AI regulation" OR "AI future" OR "AI impact" OR "AI development" OR "AI technology" '
        'OR "AI research") -is:retweet -soccer -football -betting -sports -airdrop -token -reward -promotion -#crypto '
        '-#blockchain -#bitcoin -crypto -#NFT -#DeFi -web3 -gaming -#sportsgambling -#baseball -has:links -has:mentions  lang:en'
    )

    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=['created_at', 'author_id', 'text', 'id'],
            max_results=max_results,
            start_time=start_time
        )
        print("Tweets retrieved successfully.")
        return response
    except tweepy.errors.TweepyException as e:
        print(f"Failed to retrieve tweets: {e}")
        return None

def save_tweets(response, job_id, channel):
    rows_processed = 0
    rows_failed = 0

    if response and response.data:
        # Iterate through tweets, but filter out tweets with cashtags -- we can't do this through the api so this next best option
        for tweet in [tweet for tweet in response.data if not re.search(r'\$\w+', tweet.text)]:
            try:
                # Create a message payload
                message_payload = {
                    'id': str(tweet.id),
                    'author_id': str(tweet.author_id),
                    'text': tweet.text.replace('\n', ' '),
                    'created_at': tweet.created_at.isoformat(),
                    'collector_job_id': job_id
                }
                # Serialize the message payload to a JSON string
                message_payload_str = json.dumps(message_payload)
                # Publish the message to the queue
                channel.basic_publish(
                    exchange='',
                    routing_key='message_queue',
                    body=message_payload_str
                )
                print(f"Tweet {tweet.id} added to queue.")
                rows_processed += 1
            except Exception as e:
                print(f"Failed to add tweet {tweet.id} to the queue: {e}")
                rows_failed += 1

    return rows_processed, rows_failed

def process_job():
    job = Job()
    job.id = str(uuid.uuid4())
    job.service_name = "data-collector"
    job.job_start_date = datetime.utcnow()

    session.add(job)
    session.commit()

    last_job_end_time = get_last_job_end_date("data-collector")

    bearer_token = init()
    tweets = get_tweets(10, bearer_token, last_job_end_time.strftime('%Y-%m-%dT%H:%M:%SZ') if last_job_end_time else None)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT')),
        credentials=pika.PlainCredentials(
            os.getenv('RABBITMQ_USER'),
            os.getenv('RABBITMQ_PASSWORD')
        )
    ))
    channel = connection.channel()
    channel.queue_declare(queue='message_queue')

    rows_processed, rows_failed = save_tweets(tweets, job.id, channel)

    connection.close()

    job.job_end_date = datetime.utcnow()
    job.runtime = (job.job_end_date - job.job_start_date).total_seconds() * 1000  # Convert to milliseconds
    job.rows_processed = rows_processed
    job.rows_failed = rows_failed

    session.commit()

process_job()
