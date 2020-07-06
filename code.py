#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


# In[2]:


from google.colab import drive
drive.mount('/content/gdrive')
get_ipython().run_line_magic('cd', '"/content/gdrive/My Drive"')


# In[3]:


import pandas as pd
raw_data=pd.read_csv('/var/log/apache2/access.log', sep=" ")
raw_data.to_csv('log.csv')
get_ipython().system('cat log.csv')


# 

# In[4]:


data = pd.read_csv('log2.csv', skiprows=2, names=['IP','Dash','Dash1','Date','TimeZone','Request_Header','Status_code','Byte_tansfer','Blank','Browser_Name'])
df = pd.DataFrame(data=data)
clean = df.drop(df.columns[[1,2,3,4,5,7,8,9]], axis = "columns")
clean.head(20)


# In[5]:


data12=clean.groupby(["IP", "Status_code"]).size().reset_index(name="frequency")
data12


# In[6]:


data12['IP'].value_counts()


# In[7]:


data12['Status_code'].value_counts()


# In[8]:


from sklearn.preprocessing import StandardScaler #Data Scaling
sc = StandardScaler() 
data_scaled = sc.fit_transform(data12)


# In[9]:


train_data = data12.drop(['IP'], axis=1)


# In[ ]:





# In[10]:


from sklearn.preprocessing import StandardScaler #Data Scaling
sc = StandardScaler() 
data_scaled = sc.fit_transform(train_data)
print(data_scaled)


# In[92]:


#Adding Cluster Labels to dataset
import numpy as np
from sklearn.cluster import KMeans #Creating Model 
model = KMeans(n_clusters=4) #Fit and Predict 
pred = model.fit_predict(data_scaled)

data_with_pred = pd.DataFrame(data_scaled, columns=['Status_Scaled','Frequency_scaled'])
data_with_pred['Clusters'] = pred
final_data = pd.concat([data12, data_with_pred], axis=1)
final_data


# In[73]:


final_data.plot.bar(x='IP', y='frequency', rot=0)


# In[ ]:





# In[97]:


Block_IP = []  
for key,value in final_data.iloc[:,[0,2,5]].iterrows():
  if value.frequency > 40:
    print(value.Clusters)
    print(value.IP)
    Block_IP.append(value.Clusters)
Block_IP[0]


# In[109]:


import os
for key,value in final_data.loc[:,['IP','frequency','Clusters']].iterrows():
  if value.frequency > 40:
    os.system('sudo iptables -A INPUT -s {} -p tcp --destination-port 80 -j DROP'.format(value.IP))
    print("IP blocked by system is",value.IP)


# In[ ]:




