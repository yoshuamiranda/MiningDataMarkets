#!/usr/bin/env python
# coding: utf-8

# In[88]:


#! pip install mysql-connector-python-rf
#! pip install pyyaml
#! pip install pymongo[tls]
#! pip install --upgrade certifi
#! pip install -c anaconda certifi
#!pip install boto3


# In[40]:

import mysql.connector
import yaml
import os
with open("/bedu/credentials.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)
    
    os.chdir('/bedu')
    
# In[41]:


cnx = mysql.connector.connect(
    host=params['host'],
    port=params['port'],
    user=params['user'],
    password=params['password'],
    database=params['database'],
    auth_plugin='mysql_native_password'
)


# In[42]:


cursor = cnx.cursor()
cursor.execute("SELECT idText, TweetText FROM tbl_Text WHERE Processed = 1 AND AWSSentiment = 0")
words = cursor.fetchall()
cursor.close()


# In[43]:

import json
import boto3

# In[44]:


if len(words) > 0:
    for tweet in words:
        comprehend = boto3.client(
            service_name='comprehend', 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-2')     
            
        text = tweet[1]
        if len(text) > 0:
            response = comprehend.batch_detect_sentiment(TextList=[text,], LanguageCode='es')
            x = response.get('ResultList')
            Sentiment_res = x[0]['Sentiment']
            Positive_res = x[0]['SentimentScore']['Positive']
            Negative_res = x[0]['SentimentScore']['Negative']
            Neutral_res = x[0]['SentimentScore']['Neutral']
            Mixed_res = x[0]['SentimentScore']['Mixed']
            cursor = cnx.cursor()
            sql = "INSERT INTO tbl_AWSSentiment (idText, Sentiment, Positive, Negative, Neutral, Mixed) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (tweet[0], Sentiment_res, Positive_res, Negative_res, Neutral_res, Mixed_res)
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        cursor = cnx.cursor()
        sql = "UPDATE tbl_Text set AWSSentiment = %s WHERE idText = %s"
        val = (1, tweet[0])
        cursor.execute(sql, val)
        cnx.commit()
        cursor.close()
cnx.close()

# In[10]:




