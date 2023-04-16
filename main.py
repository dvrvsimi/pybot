import tweepy
# import openai

# calling keys, secrets, tokens from config
from config import consumer_key, consumer_secret, access_token, access_token_secret, openai_key
# openai.api_key = openai_key


#Setting credentials to access Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#calling API using Tweepy
api = tweepy.API(auth, wait_on_rate_limit=True)

#search keyword 
search = 'blah'
#maximum limit of tweets to be interacted with
maxNumberOfTweets = 1

#to keep track of tweets published
count = 0

for tweet in tweepy.Cursor(api.search_tweets, search).items(maxNumberOfTweets):
    try:
        # for each status, overwrite that status by the same status, but from a different endpoint.
        status = api.get_status(tweet.id)
        if status.retweeted == False and status.favorited == False:
            count = count + 1
            print("Found tweet by @" + tweet.user.screen_name)
            print(count)
    except tweepy.errors.TweepyException as error:
        print(str(error))