#!/usr/bin/env python
# coding: utf-8

# In[88]:


#! pip install mysql-connector-python-rf
#! pip install pyyaml
#! pip install pymongo[tls]
#! pip install --upgrade certifi
#! pip install -c anaconda certifi


# In[24]:


import mysql.connector
import yaml
import os
with open("/bedu/credentials.yaml", "r") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)
    
    os.chdir('/bedu')

# In[25]:


cnx = mysql.connector.connect(
    host=params['host'],
    port=params['port'],
    user=params['user'],
    password=params['password'],
    database=params['database'],
    auth_plugin='mysql_native_password'
)


# In[ ]:





# In[26]:


cursor = cnx.cursor()
cursor.execute("SELECT w.idwords, s.idStopWords, w.Word FROM tbl_Words w LEFT JOIN tbl_StopWords s on w.Word = s.StopWord WHERE w.ProcessWord = 0 LIMIT 5000")
words = cursor.fetchall()
cursor.close()
words


# In[27]:


import pandas as pd

if len(words) > 0:
    for x in words:
        if x[1]:
            cursor = cnx.cursor()
            sql =  "UPDATE tbl_Words SET ACTIVE = %s, ProcessWord = %s WHERE idwords = %s"
            val = (0,1,x[0])
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        elif len(x[2]) < 4
            cursor = cnx.cursor()
            sql =  "UPDATE tbl_Words SET ACTIVE = %s, ProcessWord = %s WHERE idwords = %s"
            val = (0,1,x[0])
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
        else:
            cursor = cnx.cursor()
            sql =  "UPDATE tbl_Words SET ProcessWord = %s WHERE idwords = %s"
            val = (1,x[0])
            cursor.execute(sql, val)
            cnx.commit()
            cursor.close()
cnx.close()
cnx.close()


# In[28]:


len(words)


# In[ ]:




