'''
TweetMarks v0.1
Source: https://github.com/dnlongen/TweetThief
Author: David Longenecker
Author email: david@securityforrealpeople.com 
Author Twitter: @dnlongen
Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
Requires an application token for the Twitter API. See https://dev.twitter.com/oauth/overview/application-owner-access-tokens for documentation, and https://apps.twitter.com to generate your tokens

Note that the search results at twitter.com may return historical results while the Search API usually only serves tweets from the past week. See https://dev.twitter.com/rest/public/search
'''

import argparse, tweepy, sys, codecs, time, os, json

#########################################################################
# Replace the below values with your own, from https://apps.twitter.com #
consumer_key = <your consumer key>
consumer_secret = <your consumer secret>
access_token = <your access token>
access_token_secret = <your access token secret>
#########################################################################

# Define supported parameters and default values
parser = argparse.ArgumentParser(description='Extract URLs from tweets "liked" by a given alias, and add them to browser bookmarks.')
parser.add_argument('-a', '--alias', dest='twitter_alias', required=True, help='Twitter alias whose tweets to analyze')
parser.add_argument('-n', '--numtweets', default=20, type=int, help='Maximum number of tweets to analyze for specified Twitter user; default 20')
parser.add_argument('-p', '--proxy', default='', required=False, help='HTTPS proxy to use, if necessary, in the form of https://proxy.com:port')
args=parser.parse_args()
twitter_load=args.numtweets
twitter_list=[args.twitter_alias]
https_proxy=args.proxy

#Uncomment for Python 2:
#if sys.stdout.encoding != 'cp850':
#  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'xmlcharrefreplace')
#if sys.stderr.encoding != 'cp850':
#  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'xmlcharrefreplace')

#Uncomment for Python 3:
#if sys.stdout.encoding != 'cp850':
#  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
#if sys.stderr.encoding != 'cp850':
#  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

def parse_twitter(twitter_user):
    status        = ""
    for status in api.favorites(twitter_user,count=twitter_load):
      try:
        # since_id returns statuses more recent than specified ID; max_id returns statuses earlier than specified ID
        # no native way to filter user_timeline based on a time window?
        orig_user = status.user.screen_name
        orig_text = status.text
        orig_id   = str(status.id)
        orig_date = time.strftime("%Y-%b-%d %H:%M", time.strptime(str(status.created_at),"%Y-%m-%d %H:%M:%S"))
        orig_link = "https://twitter.com/" + orig_user + "/status/" + str(status.id)
        if (not status.entities["urls"] == []): # if there are urls, expand them
          for url in status.entities["urls"]:
              text=status.text
              expanded_url=url["expanded_url"]
              display_url=url["display_url"]
              print("URL: " + expanded_url + "; title: " + text)
              # to do: get title or preview for link, instead of using tweet text
              # bookmark_file = os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks" - JSON format
              # with open(bookmark_file) as data_file:
              #   bookmark_data = json.load(data_file)
              # Look for bookmark_data["roots"]["bookmark_bar"]["children"] name=Tweetmarks and type=folder
              # Filter out URLs of twitter.com/* - goal is to bookmark external URLs, not tweets
      except tweepy.TweepError as e:
        # 429 means rate-limited
        if str(e).find("status code = 429"): 
          print("Twitter API rate-limited; try again in a few minutes.")
          print("The Twitter API rate-limits requests within a 15-minute window.")
          print("Refer to https://dev.twitter.com/rest/public/rate-limiting for more information.")
          break
        print("Twitter API error. Message:")
        print(str(e))
    print("Finished processing user " + twitter_user)


#################################################################################################
# Main body
#################################################################################################

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,proxy=https_proxy)
for twitter_user in twitter_list:
    # With each Twitter handle, run through the parser routine
    # Current cmdline parameters allow for only one Twitter handle; this is to enable future enhancement
    parse_twitter(twitter_user)
