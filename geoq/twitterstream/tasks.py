from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from celery import shared_task

access_token = "3248261306-H77EHvXe48pbWdmzUawfoRhgGxQDm2VKFlnfacW"
access_token_secret = "vTrQ1DrMzAfe2GXeNycVc6oagaz3JDGW5EweinnZytZhZ"
consumer_key = "ZuPoSR6v2UW9RRUM3jVNy4lXQ"
consumer_secret = "dMDpqXNxbcCwmTJQSAYCJkFfStpotj8ZDcka1CWbUmwdTzieK6"

#This is a basic listener that just prints received tweets to file.
class TwitterStream(StreamListener):

    def on_data(self, data):
        f1 = open('../..stream.json', 'w+')
        f1.write(data)
        #return True

    def on_error(self, status):
        print status


@shared_task
def openStream(geoCode):
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TwitterStream()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(locations=[geoCode])

@shared_task
def testTask(geoCode):
    return geoCode
