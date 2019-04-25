import tweepy
import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
print('this is my twitter bot')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        userMessage = mention.full_text.lower()
        if any(srchstr in userMessage for srchstr in ('sad', 'suicide', 'suicidal','ill','help','please','self-harm','cut','kill','hang','dead','mental','health','crazy','insane','mind','losing')):
            print("found sad human")
            print('responding back.....')
            api.update_status('@'+mention.user.screen_name + " " + "please give it another day, stay alive fren ||-//\n" + "here are a list of helpline if you need a human\n" + "http://ibpf.org/resource/list-international-suicide-hotlines", mention.id)
        if any(srchstr in userMessage for srchstr in ('hello','hi','heya')):
            print('found hello')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + " "
                    'Hello back to you!', mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
