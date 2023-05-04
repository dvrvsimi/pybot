
import tweepy
import re
from config import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a Tweepy API object
api = tweepy.API(auth)

# Get the user's bookmarks and search for a keyword
try:
    mentions = api.mentions_timeline()
    #print(mentions)
except tweepy.TweepError as e:
    print(f"Error: {e}")
else:
    for mention in mentions:
        if '@dvrvsimi' in mention.text:
            try:
                keyword = re.findall(r'(?<=@dvrvsimi ).+', mention.text)[0]
                bookmarks = api.bookmarks()
                tweets = []

                for bookmark in bookmarks:
                    tweet = bookmark.tweet
                    if hasattr(tweet, 'retweeted_status'):
                        continue # Skip retweets
                    if hasattr(tweet, 'is_quote_status') and tweet.is_quote_status:
                        continue # Skip quoted tweets
                    if keyword in tweet.text:
                        tweets.append(tweet.text)

                if len(tweets) > 0:
                    user = mention.user
                    message = "Here are the tweets I found matching your query:\n\n"
                    message += "\n\n".join(tweets)
                    try:
                        api.send_direct_message(user.id, message)
                    except tweepy.TweepError as e:
                        print(f"Error: {e}")
            except IndexError:
                print("Error: invalid mention format")
            except tweepy.TweepError as e:
                print(f"Error: {e}")

try:
    user = api.verify_credentials()
    print(f"Authenticated as {user.screen_name}")
except tweepy.TweepError as e:
    print(f"Error: {e}")

