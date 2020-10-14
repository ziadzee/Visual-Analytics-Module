#!/usr/bin/env python
# coding: utf-8

# ## Visiual Analytics - Tutorial Lab 02
# 
# ### Ziad Al-Ziadi
# #### 150010258
# #### MSc Data Science
# 
# #### Bike Hire Data in London
# 
# Visiaulising two separate datasets corresponding to bike hire data in Londnon.
# 
# 
# Stations dataset :
# - id: bike station ID
# - name: area of bike station location
# - lat: station latitude
# - lon: station longtitude
# - x: location in the x axis
# - y: location in the y axis.
# 
# Bike dataset :
# - stationId: bike station ID
# - availableBikes: number of available bikes in the station
# - availableDocks: number of available docks in the station
# - t: data collection time

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt


# In[2]:


stations = pd.read_csv("bikeStationsWithOSGB.tsv", sep="\t")

stations["area"] = stations["name"].apply(lambda x: x.split(",")[1])
stations["name"] = stations["name"].apply(lambda x: x.split(",")[0])


bike = pd.read_csv("last24h.csv")


# In[3]:


bike.head()


# In[4]:


bike.describe()


# In[5]:


stations.head()


# Creating a new coloumns showing bike capacity and proporation

# In[6]:


bike["capacity"] = bike["availableBikes"] + bike["availableDocks"]
bike["proportion"] = bike["availableBikes"] / bike["capacity"]


# In[7]:


bike["t"] = pd.to_datetime(bike["t"])


# In[8]:


bike.head()


# Merging both datasets

# In[9]:


bike = pd.merge(bike, stations, left_on="stationId", right_on="id")


# In[10]:


bike.head()


# Creating a new hour column

# In[11]:


bike["hour"] = bike["t"].dt.hour


# In[12]:


alt.data_transformers.disable_max_rows() # Our dataset is >5000 therefore we need to disable Altair's max row cap


# In[13]:


# Plotting a box-plot showing hour and proporotion 

alt.Chart(bike).mark_boxplot().encode(

    x = "hour:O",
    y = "proportion:Q"

)


# In[16]:


# Plotting a box-plot showing hour and area

alt.Chart(bike).mark_boxplot().encode(

    x = "proportion:Q",
    y = "area"

)


# In[18]:


# Plotting the latitude and longtitude coodinates as a scatter plot. Notice the plot resemebles a map of London.

bike.plot(kind="scatter", x="x", y="y", s=bike["capacity"], label="Capacity",
          c="proportion", cmap=plt.get_cmap("jet"), colorbar=True, figsize=(10, 7),
          alpha=0.4)
plt.show()

