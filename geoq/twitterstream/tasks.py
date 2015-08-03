from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from celery import shared_task
from django.core.cache import cache
import json

access_token = "3248261306-H77EHvXe48pbWdmzUawfoRhgGxQDm2VKFlnfacW"
access_token_secret = "vTrQ1DrMzAfe2GXeNycVc6oagaz3JDGW5EweinnZytZhZ"
consumer_key = "ZuPoSR6v2UW9RRUM3jVNy4lXQ"
consumer_secret = "dMDpqXNxbcCwmTJQSAYCJkFfStpotj8ZDcka1CWbUmwdTzieK6"

twitter_active_key = 'twitter_stream_active'
twitter_close_key = 'twitter_close_stream'

#This is a basic listener that just prints received tweets to file.
class TwitterStream(StreamListener):
    STREAM_FILE = 'geoq/twitterstream/stream.json'

    @staticmethod
    def close_stream():
        print 'Closing stream....'
        cache.set(twitter_active_key, False)
        return False

    def on_data(self, raw_data):
        """ Overwritten method which handles when tweets come in from Twitter """
        cache.add('twitter_close_stream', True)

        tweets = []
        json_data = json.loads(raw_data)
        cache.set(twitter_active_key, True)

        # filters not English tweets
        if not (('lang' in json_data) and (json_data['lang'] == 'en')):
            return True

        with open(self.STREAM_FILE, mode='r') as feed:
            tweets = json.load(feed)
            # close stream if the file is getting too large
            if len(tweets) > 59:
                cache.set(twitter_close_key, True)
        with open(self.STREAM_FILE, mode='w') as feed:
            tweets.append(json_data)
            json.dump(tweets, feed)

        print raw_data

        # Check if stream should close, defaults to True
        # defaulting to True causes stream to terminate when cache expires
        if cache.get(twitter_close_key, True):
            return self.close_stream()

    def on_error(self, status):
        """ Overwritten method which handles when errors when connecting to Twitter """

        print status
        # returns stream.json into empty array
        with open(self.STREAM_FILE, mode='w') as f:
            f.write('[]')

        self.close_stream()

    def on_disconnect(self, notice):
        print "Disconnecting from Twitter Streaming API..."
        # returns stream.json into empty array
        with open(self.STREAM_FILE, mode='w') as f:
            f.write('[]')

        self.close_stream()


@shared_task
def openStream(geoCode):
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TwitterStream()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(locations=geoCode, async=True)

@shared_task
def testTask(geoCode):
    return geoCode

@shared_task
def clearJson():
    # guarantees empty json when stream starts
    with open(TwitterStream.STREAM_FILE, mode='w') as f:
            f.write('[]')
