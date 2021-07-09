#!/usr/bin/env python
# coding: utf-8

# In[88]:


#! pip install mysql-connector-python-rf
#! pip install pyyaml
#! pip install pymongo[tls]
#! pip install --upgrade certifi
#! pip install -c anaconda certifi


# In[150]:


import mysql.connector
import yaml
with open("/bedu/credentials.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)


# In[151]:


cnx = mysql.connector.connect(
    host=params['host'],
    port=params['port'],
    user=params['user'],
    password=params['password'],
    database=params['database'],
    auth_plugin='mysql_native_password'
)


# In[ ]:





# In[152]:


cursor = cnx.cursor()
cursor.execute("SELECT Word, ID FROM tbl_Diccionario WHERE Actived = 1")
words = cursor.fetchall()
cursor.close()
words


# In[153]:


cursor = cnx.cursor()
cursor.execute("SELECT IFNULL(max(ID_Twitter),0) FROM tbl_IDTwitter")
lastID = cursor.fetchall()
cursor.close()
lastID


# In[154]:


import pickle
import os
import yaml
with open("/bedu/credentialsTwiiter.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)
    
    
os.chdir('/bedu')


# In[155]:


if not os.path.exists('secret_twitter_credentials.pkl'):
    Twitter={}
    Twitter['Consumer Key'] = params['Consumer Key']
    Twitter['Consumer Secret'] = params['Consumer Secret']
    Twitter['Access Token'] = params['Access Token']
    Twitter['Access Token Secret'] = params['Access Token Secret'],
    with open('secret_twitter_credentials.pkl','wb') as f:
        pickle.dump(Twitter, f)
else:
    Twitter=pickle.load(open('secret_twitter_credentials.pkl','rb'))


# In[156]:


import twitter

auth = twitter.oauth.OAuth(Twitter['Access Token'],
                           Twitter['Access Token Secret'],
                           Twitter['Consumer Key'],
                           Twitter['Consumer Secret'])

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print(twitter_api)


# In[157]:


import re
def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# In[158]:


import json
import pymongo
import pandas as pd
from pymongo import MongoClient
import datetime
import ssl 

with open("credentials.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

client = MongoClient(params['Mongoinfo'], 27017, ssl_cert_reqs=ssl.CERT_NONE)
db = client['Bedu_Project']
collection_currency = db['JSON_tweets']

x = 0
for i in words:
    hashtagt = i
    #hashtag = '#' + hashtagt[0]
    hashtag = hashtagt[0]
    number = 1000
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=hashtag, count= 100, since_id= lastID)
    statuses = search_results['statuses']
    if len(statuses) > 0:
        collection_currency.insert_many(statuses)
        cursor = cnx.cursor()
        status_texts = [ status['text'] 
                 for status in statuses
                    if status['retweet_count'] == 0]
        sql = "CALL sp_loginsert(%s, %s, %s);"
        val = (hashtagt[1], len(statuses), len(status_texts))
        cursor.execute(sql, val)
        cnx.commit()
        cursor.close()
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(idLog) FROM tbl_Log")
        idlog = cursor.fetchall()
        cursor.close()
        status_ID = [ status['id'] 
                 for status in statuses 
                    if status['retweet_count'] == 0]
        status_hashtag = [ status['entities']['hashtags']
                 for status in statuses
                    if status['retweet_count'] == 0]
        hashtags = [ hashtag['text'] 
             for status in statuses
                 for hashtag in status['entities']['hashtags'] 
                   if status['retweet_count'] == 0]
        wordsintweets = [ clean_tweet(w) 
          for t in status_texts 
              for w in t.split()]
        users = [ status['user']['screen_name']
                 for status in statuses]
        
        created = datetime.datetime.now()
        #insert Tweeter ID into tables
        for x in status_ID:
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_IDTwitter (ID_Twitter, IdLog, Created) VALUES (%s, %s, %s)"
            val = (x, idlog[0][0], created)
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        #insert HAstags from tweets
        for x in hashtags:
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_Hashtag (Hashtag, IdLog, Created) VALUES (%s, %s, %s)"
            val = (x, idlog[0][0], created)
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        #insert words fro tweets
        for x in wordsintweets:
            if len(x)> 0:
                cursor = cnx.cursor()
                sql = "INSERT INTO tbl_Words (word, IdLog, Created) VALUES (%s, %s, %s)"
                val = (x, idlog[0][0], created)
                cursor.execute(sql, val)
                cnx.commit()
                cursor.close()
        for x in status_texts:
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_Text (IDLog, TweetText, Seintiment, SeintimentDate, Processed) VALUES (%s, %s, %s, %s, %s)"
            val = (idlog[0][0], clean_tweet(x), 0, created, 0)
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        for x in users:
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_userstwitter (IDLog, userstwitter,userstwitterDate) VALUES (%s, %s, %s)"
            val = (idlog[0][0], clean_tweet(x), created)
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        for info in statuses:
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_RetweetsFav (idTweet, Retweet, Favs) VALUES (%s, %s, %s)"
            val = (info['id'], info['retweet_count'], info['favorite_count'] )
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
    else:
        cursor = cnx.cursor()
        sql = "CALL sp_loginsert(%s, %s);"
        val = (1, 10)
        cursor.execute(sql, val)
        cnx.commit()
        cursor.close()
client.close()
cnx.close()


# In[ ]:




