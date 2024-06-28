import tweepy

class TwitterClient:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)

    def search_tweets(self, query, max_results=10):
        try:
            response = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['created_at', 'author_id', 'text', 'id', 'lang'],
                max_results=max_results
            )
            return response.data
        except tweepy.errors.TweepyException as e:
            print(f"Failed to retrieve tweets: {e}")
            return None
