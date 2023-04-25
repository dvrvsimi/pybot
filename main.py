import tweepy
import openai

# calling keys, secrets, tokens from config
from config import consumer_key, consumer_secret, access_token, access_token_secret, openai_key
openai.api_key = openai_key


#Setting credentials to access Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#calling API using Tweepy
api = tweepy.API(auth, wait_on_rate_limit=True)

#search keyword 
search = []
#maximum limit of tweets to be interacted with
maxNumberOfTweets = 1
#to keep track of tweets published
count = 0

for tweet in tweepy.Cursor(api.search_tweets, search).items(maxNumberOfTweets):
    try:
        status = api.get_status(tweet.id)
        if status.retweeted == False and status.favorited == False:
            count = count + 1
            print("Found tweet by @/" + tweet.user.screen_name)
            user_in = ("did" + tweet.user.screen_name + "tweet" + input(search) + "?")
            print(count)
    except tweepy.errors.TweepyException as error:
        print(str(error))

        
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": input('question 1 ')},
        {"role": "assistant", "content": ""},
        {"role": "user", "content": tweet.text}
    ]tests
)
print(response['choices'][0]['message']['content'])