import tweepy
import os

import getCurrentData


def main():    
    twitter_auth_keys = {
        "consumer_key"        : os.getenv("TWITTER_CONSUMER_API_KEY"),
        "consumer_secret"     : os.getenv("TWITTER_CONSUMER_API_SECRET"),
        "access_token"        : os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_token_secret" : os.getenv("TWITTER_ACCESS_TOKEN_SECRET") 
    }

    client = tweepy.Client(consumer_key=twitter_auth_keys['consumer_key'],
                        consumer_secret= twitter_auth_keys['consumer_secret'],
                        access_token=twitter_auth_keys['access_token'],
                        access_token_secret=twitter_auth_keys['access_token_secret']
      )
    

    tweet = getCurrentData.main()
    print(tweet)
    
    try:
        client.create_tweet(text=tweet)
    except Exception as e:
        print(e)
        print("Tweet failed")
        
    
if __name__ == "__main__":
    main()