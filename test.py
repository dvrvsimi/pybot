# import tweepy
# import openai
# import json
# import time
# # import pandas as pd
# import re

# # calling keys, secrets, tokens from config



# # #Setting credentials to access Twitter API and scope for bookmark
# # auth = tweepy.OAuth2UserHandler(
# #     scope=["bookmark.read", "bookmark.write", "tweet.read", "users.read"],
# #     redirect_uri = 'https://127.0.0.1:6006/callback', client_id=client_ID, client_secret=client_secret
# #     )
# # # auth.set_access_token(access_token, access_token_secret)

# # print(auth.get_authorization_url())



# # verifier = "https://oauth.pstmn.io/v1/browser-callback"
# # access_token = auth.fetch_token(verifier)

# # print(f"\naccess-token-pkce={access_token['access_token']}")


# # access_token_pkce = access_token

# # client = tweepy.Client(access_token)

# # some_tweet = "1536895050176667649"
# # # add tweet to bookmarks
# # response = client.bookmark(tweet_id=some_tweet )
# # print(f"Tweet {some_tweet} bookmarked: {response.data['bookmarked']}")


# # print('zoo wee mama')

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# mentions = api.mentions_timeline()

# for mention in mentions:
#     if '@bookmark_io' in mention.text:
#         keyword = re.findall(r'(?<=@bookmark_io ).+', mention.text)[0]
#         bookmarks = api.bookmarks()
#         tweets = []

#         for bookmark in bookmarks:
#             tweet = bookmark.tweet
#             if hasattr(tweet, 'retweeted_status'):
#                 continue # Skip retweets
#             if hasattr(tweet, 'is_quote_status') and tweet.is_quote_status:
#                 continue # Skip quoted tweets
#             if keyword.lower() in tweet.text.lower():
#                 tweets.append(tweet.text)

#         if len(tweets) > 0:
#             user = mention.user
#             message = "Here are the tweets I found matching your query:\n\n"
#             message += "\n\n".join(tweets)
#             print(api.send_direct_message(user.id, message))

# print(mentions)

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
        if '@bookmark_io' in mention.text:
            try:
                keyword = re.findall(r'(?<=@bookmark_io ).+', mention.text)[0]
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


