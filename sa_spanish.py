#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install sentiment-analysis-spanish


# In[2]:


#pip install keras tensorflow


# In[14]:
import os
os.chdir('/bedu')

import mysql.connector
import yaml
with open("/bedu/credentials.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)


# In[16]:


cnx = mysql.connector.connect(
    host=params['host'],
    port=params['port'],
    user=params['user'],
    password=params['password'],
    database=params['database'],
    auth_plugin='mysql_native_password'
)


# In[17]:


from sentiment_analysis_spanish import sentiment_analysis


# In[18]:


cursor = cnx.cursor()
cursor.execute("SELECT idText, TweetText FROM tbl_Text WHERE Processed = 0")
text = cursor.fetchall()
cursor.close()
text


# In[19]:


if len(text) > 0:
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    for i in text:
        num = sentiment.sentiment(i[1])
        y = num.item()
        cursor = cnx.cursor()
        sql = "UPDATE tbl_Text SET Seintiment = %s, Processed = 1 WHERE idText =%s"
        val = (y, i[0])
        cursor.execute(sql, val)
        cnx.commit()
        cursor.close()
cnx.close()


# In[ ]:




