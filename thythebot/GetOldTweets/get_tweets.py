import got
import csv

def main():

    def printTweet(descr, t):
        print descr
        print "Username: %s" % t.username
        print "Retweets: %d" % t.retweets
        print "Text: %s" % t.text
        print "Mentions: %s" % t.mentions
        print "Hashtags: %s\n" % t.hashtags
        print "Time: %s\n" % t.date

    #Get tweets by query search, change the max tweets accordingly
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('tayandyou').setSince("2016-03-23").setUntil("2016-03-24").setMaxTweets(60000)

    print len(got.manager.TweetManager.getTweets(tweetCriteria))

    with open('tweets_mar23_mar24_from_website.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['User Name','ReTweets','Text','Mentions','Hashtags','Time'])

        for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
            printTweet("### Example 2 - Get tweets by query search [tayandyou]", tweet)
            #print tweet
            try:
                #if tweet['created_at'].find('Mar 23')!=-1 or tweet['created_at'].find('Mar 24')!=-1:
                spamwriter.writerow([tweet.username,tweet.retweets,tweet.text,tweet.mentions,tweet.hashtags,tweet.date])
            except UnicodeEncodeError:
                print "Unicode Error",tweet['user']['screen_name'],tweet['text'],tweet['created_at']

if __name__ == '__main__':
    main()
