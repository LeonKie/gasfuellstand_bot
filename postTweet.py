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
    
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
 

    tweet = getCurrentData.main()

    

    
   
    
    try:
        api.update_status(status=tweet)
    except Exception as e:
        print(e)
        print("Tweet failed")
        
    
if __name__ == "__main__":
    main()