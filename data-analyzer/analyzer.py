import os
import json
import pika
from datetime import datetime
from google.cloud import language_v1
from db import session, Base, engine
from models.message import Message
from models.job import Job
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

def init():
    load_dotenv()
    Base.metadata.create_all(engine)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    score = sentiment.score
    magnitude = sentiment.magnitude
    sentiment_text = 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
    magnitude_text = 'low' if magnitude < 1 else 'medium' if magnitude < 2 else 'high'
    return score, magnitude, sentiment_text, magnitude_text

def process_tweet(ch, method, properties, body):
    try:
        data = json.loads(body)
        tweet_id = data['id']
        tweet = session.query(Message).get(tweet_id)

        if tweet is None:
            # If the tweet is not found, create a new tweet
            tweet = Message(
                id=tweet_id,
                author_id=data['author_id'],
                text=data['text'],
                created_at=datetime.fromisoformat(data['created_at']),
                processed=False,
                collector_job_id=data['collector_job_id']
            )
            session.add(tweet)
            print(f"Added tweet {tweet_id} to the database.")

        if not tweet.processed:
            score, magnitude, sentiment_text, magnitude_text = analyze_sentiment(tweet.text)
            tweet.sentiment_score = score
            tweet.sentiment_magnitude = magnitude
            tweet.sentiment_text = sentiment_text
            tweet.sentiment_classification = sentiment_text
            tweet.magnitude_classification = magnitude_text
            tweet.processed = True
            tweet.analyzer_job_id = data['collector_job_id']  # Link to the same job ID

            session.commit()
            print(f"Processed tweet {tweet_id} successfully.")
        else:
            print(f"Tweet {tweet_id} not found or already processed.")
    except SQLAlchemyError as e:
        print(f"Failed to process tweet {tweet_id}: {e}")
        session.rollback()
    except json.JSONDecodeError as e:
        print(f"Failed to decode message: {e}")

def start_analyzer():
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

    channel.basic_consume(
        queue='message_queue',
        on_message_callback=process_tweet,
        auto_ack=True
    )

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

init()
start_analyzer()
