#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


liquor = pd.read_csv(
    "./code/datasets/Liquor_Authority_Current_List_of_Active_Licenses.csv", low_memory=False)


# In[4]:


liquor.head()



# In[5]:


authorised_liquor_store = liquor[['Serial Number', 'License Type Code', 'License Class Code', 'Certificate Number'
                                 , 'Premise Name', 'DBA','License Issued Date', 'License Expiration Date', 'Method of Operation'
                                 ]] 


# In[6]:


liquor['Premise Address 2'].unique()


# In[7]:


liquor_address = liquor[['Serial Number', 'Premise Address', 'Premise City' ,'Premise State', 'Premise Zip', 'Georeference' ]]


# In[8]:


liquor_county_zip = liquor[['Premise Zip', 'County' ]]


# In[ ]:





# In[9]:


farmers = pd.read_csv(
    "./code/datasets/Farmers__Markets_in_New_York_State.csv", low_memory=False)
farmers.head()


# In[10]:


farmers_market = farmers[['Market Name', 'Address Line 1', 'City' , 'Zip', 'Contact', 'State'
                         ,'Phone', 'Market Link', 'Operation Hours', 'Operation Season', 
                         'Operating Months', 'FMNP', 'SNAP', 'FCC Issued', 'FCC Accepted', 'Latitude','Longitude' ]]


# In[11]:


farmer_county_zip = farmers[['Zip', 'County']]


# In[ ]:





# In[12]:


retail = pd.read_csv(
    "./code/datasets/Retail_Food_Stores.csv", low_memory=False)
retail.head()


# In[13]:


# retail_food_stores = retail[['License Number', 'Establishment Type', '']]


# In[14]:


retail_food_stores = retail[['License Number', 'Establishment Type', 'Entity Name', 
                            'DBA Name', 'Street Number', 'Street Name', 'City', 
                           'State', 'Operation Type', 'Zip Code', 'Square Footage'  ]]


# In[15]:


retail_county_zip = retail[['Zip Code', 'County']]


# In[ ]:





# In[16]:


state_zip = pd.read_csv(
    "./code/datasets/New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv", low_memory=False)


# In[17]:


new_york_state_zip_code = state_zip[['State FIPS', 'County Code', 'ZIP Code', 'File Date']]


# In[18]:


state_zip.head()


# In[19]:


county_name_code = state_zip[['County Name', 'County Code']]


# In[20]:


county_zip =state_zip[['ZIP Code', 'County Name']]


# In[21]:




# now have to make global_county_zip_code
# county_zip , retail_county_zip , farmer_county_zip
# liquor_county_zip
county_zip.columns =['zip', 'county']
retail_county_zip.columns =['zip', 'county']
farmer_county_zip.columns =['zip', 'county']
liquor_county_zip.columns =['zip', 'county']


# In[22]:


frames = [county_zip, retail_county_zip, farmer_county_zip,liquor_county_zip ]

global_county_zip_code = pd.concat(frames)


# In[23]:


global_county_zip_code.shape


# In[24]:


global_county_zip_code=global_county_zip_code.drop_duplicates(subset='zip')


# In[27]:


global_county_zip_code.shape


# In[26]:


for row in global_county_zip_code:
    print( row)


# In[ ]:





# In[28]:





# In[31]:


global_county_zip_code.to_csv('./code/datasets/global_county_zip_code.csv')
county_name_code.to_csv('./code/datasets/county_name_code.csv')
retail_food_stores.to_csv('./code/datasets/retail_food_stores.csv')
authorised_liquor_store.to_csv('./code/datasets/authorised_liquor_store.csv')
liquor_address.to_csv('./code/datasets/liquor_address.csv')
farmers_market.to_csv('./code/datasets/farmers_market.csv')
new_york_state_zip_code.to_csv('./code/datasets/new_york_state_zip_code.csv')


# In[ ]:




