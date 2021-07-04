    # -*- coding: utf-8 -*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
access_token ="1402287440023277568-RePEWTgJmit4o3UVYQdZqESVU2Oztd"
access_token_secret ="i9k1P4Ox4G2EgjNS8nAiDHzTslMWby4HZAPlfZ7LZfpC5"
consumer_key = "pYAPU1aPWd15jGilSXijUXw5Z"
consumer_secret ="5EF2QwnuLuvd2m6vccy6mAACBMbPtCGbt97hWakaZQ6xrvsrNi"
file2write=open("twitter_data.txt",'w')
i=0;
#no of tweets need to load 
no_tweets=100
lines=[]
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
   
    def on_data(self, data):
        
      
        global i
        global no_tweets
        
        if i>no_tweets:  
            return False
        else:      
            file2write.write(data)
            print("tweet %s Loaded..."%i)
            i+=1
            return True
        

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(languages=["en"],track=['AustrianGP'])
    file2write.close()