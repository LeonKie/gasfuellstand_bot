import tweepy
import os
from datetime import date ,timedelta



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
 
    #tweet = "Another day, another #scifi #book and a cup of #coffee"
    #status = api.update_status(status=tweet)

    name = 'gasfuellstand'
    
    
    
    # check if tweet has already been used
    reply_id=[]
    if os.path.isfile("reply_ids.pkl"):
        with open("reply_ids.pkl", "rb") as f:
            reply_id=pickle.load(f)
            print("Loaded reply_ids.pkl", reply_id)

    points2flip = []
    for reply in replies:
        if reply.id not in reply_id:
            newCoord=extract_Coords.main(reply.text)
            if isinstance(newCoord[0], list):
                points2flip.extend(newCoord) #extract the coordinates from the tweet
            else:
                points2flip.append(newCoord)
    
    # Save the reply ids to a file
    with open('reply_ids.pkl', 'wb') as f:
        reply_id = [reply.id for reply in replies]
        pickle.dump(reply_id, f)
    
    # Create the FLIP_DOT_DISPLAY object and update the board
    board = FLIP_DOT_DISPLAY()
    board.load_board()
    
    print("This points will be flipped:" , points2flip)
    for point in points2flip:
        board.flip_a_dot(point)
        
    board.save_board()
    
    
    # Publish the board to Twitter
    tweet = board.__repr__()
    print(tweet)
    
    try:
        status = api.update_status(status=tweet)
    except:
        print("Tweet failed")
        
    
if __name__ == "__main__":
    main()